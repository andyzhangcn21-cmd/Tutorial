export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64

-- show all
hadoop jar hadoop-mapreduce-examples.jar

-- source code
https://github.com/apache/hadoop/tree/trunk/hadoop-mapreduce-project/hadoop-mapreduce-examples/src/main/java/org/apache/hadoop/examples

-- wordcount
mkdir input; mkdir output
wget -O input/books.txt https://www.gutenberg.org/files/1342/1342-0.txt
hadoop-3.4.2/bin/hadoop jar hadoop-3.4.2/share/hadoop/mapreduce/hadoop-mapreduce-examples-3.4.2.jar wordcount ~/input/input.txt ~/output/out

-- grep
cp etc/hadoop/*.xml input
grep input output 'dfs[a-z.]+'
cat output/*