rem "This is a homework 1 in 200-Python for Data Science"
rem "Author: Praba Santhanakrishnan"
rem "Created : Jan 16 2018"
mkdir s1
mkdir s1\s3
mkdir s1\s2
mkdir s1\s2\Advanced
@echo "I love bash scripting." >> s1\s3\conf.txt
@echo "A whole new world" >> s1\s2\text_chunk1.txt
@echo "A new fantastic point of view" >> s1\s2\text_chunk1.txt
copy s1\s2\text_chunk1.txt s1\s2\Advanced\text_chunk2.txt
@echo "Do you want to build a snowman?" >> s1\s2\Advanced\text_chunk2.txt
