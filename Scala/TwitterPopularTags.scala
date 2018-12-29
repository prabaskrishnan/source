/*
 * Licensed to the Apache Software Foundation (ASF) under one or more
 * contributor license agreements.  See the NOTICE file distributed with
 * this work for additional information regarding copyright ownership.
 * The ASF licenses this file to You under the Apache License, Version 2.0
 * (the "License"); you may not use this file except in compliance with
 * the License.  You may obtain a copy of the License at
 *
 *    http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

// scalastyle:off println
package org.apache.spark.examples.streaming.twitter

import org.apache.log4j.{Level, Logger}

import org.apache.spark.streaming.{Seconds, StreamingContext}
import org.apache.spark.streaming.twitter._
import org.apache.spark.SparkConf

/**
 * Calculates popular hashtags (topics) over sliding 10 and 60 second windows from a Twitter
 * stream. The stream is instantiated with credentials and optionally filters supplied by the
 * command line arguments.
 *
 * Run this on your local machine as
 *
 */
object TwitterPopularTags {

// Class to hold parsed tweets

case class parsedTweets(tag:String, userNames:Array[String], references:Array[String]) {
	def +(other:parsedTweets) : parsedTweets = {
		val allUsers = userNames ++ other.userNames
		val allreferences = references ++ other.references
		new parsedTweets(tag, allUsers.distinct, allreferences.distinct)
	}
  }


  def main(args: Array[String]) {
    if (args.length < 4) {
      System.err.println("Usage: TwitterPopularTags <consumer key> <consumer secret> " +
        "<access token> <access token secret> [<filters>]")
      System.exit(1)
    }

    // Set logging level if log4j not configured (override by adding log4j.properties to classpath)
    if (!Logger.getRootLogger.getAllAppenders.hasMoreElements) {
      Logger.getRootLogger.setLevel(Level.WARN)
    }

    val Array(consumerKey, consumerSecret, accessToken, accessTokenSecret) = args.take(4)
    val filters = args.takeRight(args.length - 4)

    // Set the system properties so that Twitter4j library used by twitter stream
    // can use them to generate OAuth credentials
    System.setProperty("twitter4j.oauth.consumerKey", consumerKey)
    System.setProperty("twitter4j.oauth.consumerSecret", consumerSecret)
    System.setProperty("twitter4j.oauth.accessToken", accessToken)
    System.setProperty("twitter4j.oauth.accessTokenSecret", accessTokenSecret)

    val sparkConf = new SparkConf().setAppName("TwitterPopularTags")

    // check Spark configuration for master URL, set it to local if not configured
    if (!sparkConf.contains("spark.master")) {
      sparkConf.setMaster("local[2]")
    }

    val ssc = new StreamingContext(sparkConf, Seconds(2))
    val sc = ssc.sparkContext

//Remove all the noisy Warning messages from the spark outputs

    sc.setLogLevel("ERROR")

//Get only English Tweets

    val stream = TwitterUtils.createStream(ssc, None, filters).filter(_.getLang == "en")


   val tweetData = stream.flatMap(status => {
			val userName = "@" + status.getUser.getScreenName
			val hashtags = status.getText.split(" ").filter(_.startsWith("#"))
			val references = status.getText.split(" ").filter(_.startsWith("@"))
			hashtags.map(tag =>	(tag, new parsedTweets(tag, Array(userName), references)))
		})

  
  val tweetDataShort = tweetData.reduceByKeyAndWindow(_ + _, Seconds(120)).map{case (tag, data) =>
                val count = data.userNames.length
                (count, data)
        }.transform(_.sortByKey(false))
 
  val tweetDataLong = tweetData.reduceByKeyAndWindow(_ + _, Seconds(1800)).map{case (tag, data) =>
                val count = data.userNames.length
                (count, data)
        }.transform(_.sortByKey(false))




	tweetDataShort.foreachRDD(rdd => {

//Take top 10 
		val top10 = rdd.take(10)
		println("\nPopular 10 hashtags in last %d seconds (%s total):\n".format(120, rdd.count()))
                println("---------------------------------------------------------------")
		top10.foreach{case (count, data) => 
			val userName = data.userNames.mkString(" ")
			val references = data.references.mkString(" ")
			println("Hashtag:  %s (%s tweets)".format(data.tag, count))
			println("Authors:  " + userName)
			println("Other Users: " + references)
			println("\n")
		}
	})



	tweetDataLong.foreachRDD(rdd => {
		val top10 = rdd.take(10)
		println("\nPopular 10 hashtags in last %d seconds (%s total):\n".format(1800, rdd.count()))
		println("---------------------------------------------------------------")
		top10.foreach{case (count, data) => 
			val userNames = data.userNames.mkString(" ")
			val references = data.references.mkString(" ")
			println("Hashtag:  %s (%s tweets)".format(data.tag, count))
			println("Authors:  " + userNames)
			println("Other Users: " + references)
                        println("\n")
		}
	})


    ssc.start()
    ssc.awaitTermination()
  }
}
