[![](https://images.microbadger.com/badges/image/goliasz/mlaas-cfreco-mini.svg)](https://microbadger.com/images/goliasz/mlaas-cfreco-mini "Get your own image badge on microbadger.com")
[![](https://images.microbadger.com/badges/version/goliasz/mlaas-cfreco-mini.svg)](https://microbadger.com/images/goliasz/mlaas-cfreco-mini "Get your own version badge on microbadger.com")

# mlaas-cfreco-mini

Fast in memory item-item recommendation engine based on https://pypi.python.org/pypi/cf_recommender/1.0.1 library.

# Container Startup

```
$ docker run -d --name=cfreco --hostname=cfreco -p 0.0.0.0:5000:5000 goliasz/mlaas-cfreco-mini
```

# Training

```
$ docker exec -it cfreco bash
# python /Preco/src/main/python/train.py --src=/Preco/data/courseInfo_with_cookie.json --recourl=http://localhost:5000/api/v1.0/router
```
## Simple Training Script

```
# python /Preco/src/main/python/train_simple.py --input=/Preco/data/sample_training.json --recourl=http://localhost:5000/api/v1.0/router
```

# Query

```
$ docker exec -it cfreco bash
# python /Preco/src/main/python/query.py --recourl=http://localhost:5000/api/v1.0/router --items=2
```

# License
Apache License, Version 2.0
