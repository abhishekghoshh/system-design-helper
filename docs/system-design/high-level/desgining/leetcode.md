# Leetcode Design

## Youtube

- [System Design Interview: Design LeetCode w/ a Google Engineer](https://www.youtube.com/watch?v=hRnJxPeoZyg)
- [System Design Interview: Design LeetCode](https://www.youtube.com/watch?v=yXr_bIl9tos)



## Problems

- [Design LeetCode](https://systemdesignschool.io/problems/leetcode)




## Scratchpad

```
for code evaluation service there can be 2 possible ways

1. use a message queue -> code execution worker (n instances) -> pick up the use code and the test cases and run it -> save the results in evaluation database

2. if it is a kubernetes service -> spawn kubernetes job -> use Kubernetes native Kueue to limit the number of jobs to be spawned -> once the jobs are spawned then pick up the use code and the test cases and run it -> save the results in evaluation database


```

