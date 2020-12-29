# 数据库服务启动流程
1. ./mongod --dbpath /.../data --logpath /.../log/mongod.log --port xxxx --bind_ip_all --fork --replSet rs0
2. ./mongo ip:port
3. rs.initiate()    
    ok = 1