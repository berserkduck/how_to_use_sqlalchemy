## 项目介绍

本项目使用[力扣数据库题目](https://leetcode.cn/problemset/database/)让使用者熟悉 [SQLAlchemy 2.0 ](https://docs.sqlalchemy.org/en/20/)的编程接口

leetcode目录中的每个模块对应一道力扣数据库题目，模块内提供以下内容：

- 题目的链接和描述
- ORM 模型
- Solution 类，提供一个通过在线测试的 SQL 解法和 SQL 对应的 ORM 解法

运行模块可查看示例数据的查询结果

## 使用方法

以 [175. 组合两个表](https://leetcode.cn/problems/combine-two-tables/description/) 为例

初始化环境

```bash
pdm init
```

安装依赖

```bash
pdm install
```

运行模块

```bash
pdm run python .\leetcode\175_combine_two_tables.py
```

## 已完成的题目

| 题目                                                                                                            | 知识点                                           |
| --------------------------------------------------------------------------------------------------------------- | ------------------------------------------------ |
| [175. 组合两个表](https://leetcode.cn/problems/combine-two-tables/description/)                                 | 左外连接                                         |
| [176. 第二高的薪水](https://leetcode.cn/problems/second-highest-salary/description/)                            | 子查询、distinct、排序、分页、别名               |
| [178. 分数排名](https://leetcode.cn/problems/rank-scores/description/)                                          | dense_rank                                       |
| [180. 连续出现的数字](https://leetcode.cn/problems/consecutive-numbers/description/)                            | 子查询、row_number、别名、分组、having、distinct |
| [181. 超过经理收入的员工](https://leetcode.cn/problems/employees-earning-more-than-their-managers/description/) | 自连接、别名                                     |
| [182. 查找重复的电子邮箱](https://leetcode.cn/problems/duplicate-emails/)                                       | 分组、having、count                              |
| [183. 从不订购的客户](https://leetcode.cn/problems/customers-who-never-order/description/)                     | 左外连接、is null                               |
| [184. 部门工资最高的员工](https://leetcode.cn/problems/department-highest-salary/description/)                  | 子查询、dense_rank、外连接                       |
| [185. 部门工资前三高的员工](https://leetcode.cn/problems/department-top-three-salaries/description/)            | 子查询、dense_rank、内连接                       |
| [196. 删除重复的电子邮件](https://leetcode.cn/problems/delete-duplicate-emails/description/)                   | 自连接、delete、子查询                          |
| [197. 上升的温度](https://leetcode.cn/problems/rising-temperature/description/)                                | 自连接、func.date()、日期处理                   |
| [595. 大的国家](https://leetcode.cn/problems/big-countries/description/)                                        | or                                               |

## 参考资料

[SQLAlchemy 2.0 Documentation](https://docs.sqlalchemy.org/en/20/)

[SQLAlchemy 2.0 文档](https://docs.sqlalchemy.org.cn)
