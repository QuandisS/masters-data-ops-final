Пример 1
```bash
❯ curl -X POST "http://localhost:8000/api/v1/predict" \
  -H "Content-Type: application/json" \
  -d '{"age": 0.1, "sex": 0.05, "bmi": 0.2, "bp": 0.3, "s1": 0.4, "s2": 0.5, "s3": 0.6, "s4": 0.7, "s5": 0.8, "s6": 0.9}'
{"predict":99.63}%  
```

Пример 2
```bash
❯ curl -X POST "http://localhost:8000/api/v1/predict" \
  -H "Content-Type: application/json" \
  -d '{"age": 18, "sex": 2, "bmi": 0.11, "bp": 0.34, "s1": 0.7, "s2": 0.1, "s3": 0.6, "s4": 0.6, "s5": 0.8, "s6": 0.2334}'
{"predict":97.93}%   
```