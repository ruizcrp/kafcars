######### Installing zookeper and kafka
wget https://dlcdn.apache.org/zookeeper/zookeeper-3.8.0/apache-zookeeper-3.8.0-bin.tar.gz
mkdir zoo
tar -zxf apache-zookeeper-3.8.0-bin.tar.gz --one-top-level=zoo --strip-components 1
rm apache-zookeeper-3.8.0-bin.tar.gz
cd zoo
mkdir data
echo -e "tickTime=2000\ndataDir=`pwd`/data\nclientPort=2181\ninitLimit=5\nsyncLimit=2" > conf/zoo.cfg
cd ..
wget https://dlcdn.apache.org/kafka/3.3.1/kafka_2.13-3.3.1.tgz
mkdir kafka
tar -zxf kafka_2.13-3.3.1.tgz --one-top-level=kafka --strip-components 1
rm kafka_2.13-3.3.1.tgz

######### single multi-nodes brokers config
cp kafka/config/server.properties kafka/config/server-one.properties
cp kafka/config/server.properties kafka/config/server-two.properties
sed -i s/"broker.id=0"/"broker.id=1"/ kafka/config/server-one.properties
sed -i s/"broker.id=0"/"broker.id=2"/ kafka/config/server-two.properties
sed -i s/"log.dirs=\/tmp\/kafka-logs"/"log.dirs=\/tmp\/kafka-logs-1"/ kafka/config/server-one.properties
sed -i s/"log.dirs=\/tmp\/kafka-logs"/"log.dirs=\/tmp\/kafka-logs-2"/ kafka/config/server-two.properties
sed -i s/"broker.id=0"/"broker.id=2"/ kafka/config/server-two.properties
sed -i s/"#listeners=PLAINTEXT:\/\/:9092"/"listeners=PLAINTEXT:\/\/:9093"/ kafka/config/server-one.properties
sed -i s/"#listeners=PLAINTEXT:\/\/:9092"/"listeners=PLAINTEXT:\/\/:9094"/ kafka/config/server-two.properties

#########  launch zoo and brokers
zoo/bin/zkServer.sh start
kafka/bin/kafka-server-start.sh -daemon kafka/config/server.properties
kafka/bin/kafka-server-start.sh -daemon kafka/config/server-one.properties
kafka/bin/kafka-server-start.sh -daemon kafka/config/server-two.properties
##### check
jps
