web: gunicorn newstoday.wsgi --log-file - 
# 기본 값
web: gunicorn newstoday.wsgi --timeout 10000
# 배포하실 때 크롤링을 사용하셔야 한다면 timeout 시간을 늘려주셔야 합니다.
# Heroku에서 Default 값이 30이기 때문에 30초가 지나면 timeout 에러를 발생시키기 때문입니다.