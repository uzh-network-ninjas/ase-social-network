# how to test this?
- firstly build the docker image with the following command:
```bash
docker build -t seed_database . && docker run  -d --net=host --name seed_database seed_database
```
!! you need to add BASE_URL as env

## ! if needed you need to delete the database manually