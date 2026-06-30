"""
https://leetcode.cn/problems/duplicate-emails/description/

表: Person

+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| id          | int     |
| email       | varchar |
+-------------+---------+
id 是该表的主键（具有唯一值的列）。
此表的每一行都包含一封电子邮件。电子邮件不包含大写字母。



编写解决方案来报告所有重复的电子邮件。 请注意，可以保证电子邮件字段不为 NULL。

以 任意顺序 返回结果表。

结果格式如下例。



示例 1:

输入:
Person 表:
+----+---------+
| id | email   |
+----+---------+
| 1  | a@b.com |
| 2  | c@d.com |
| 3  | a@b.com |
+----+---------+
输出:
+---------+
| Email   |
+---------+
| a@b.com |
+---------+
解释: a@b.com 出现了两次。

"""

from sqlalchemy import String, select, text, func, ChunkedIteratorResult
from sqlalchemy.orm import Session, Mapped, mapped_column
from db import Base, engine
from utils import print_tabulate_formatted_result


class Person(Base):
    __tablename__ = "person"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255))


Base.metadata.create_all(engine)


class Solution:
    def sql(self, session: Session) -> ChunkedIteratorResult:
        result = session.execute(
            text("select email from person group by email having count(email) > 1")
        )
        return result

    def orm(self, session: Session) -> ChunkedIteratorResult:
        stmt = (
            select(Person.email)
            .group_by(Person.email)
            .having(func.count(Person.email) > 1)
        )
        result = session.execute(stmt)
        return result


if __name__ == "__main__":
    with Session(engine) as session:
        persons = [{"email": "a@b.com"}, {"email": "c@d.com"}, {"email": "a@b.com"}]

        for i in range(len(persons)):
            person = Person(**persons[i])
            session.add(person)

        session.commit()

        print_tabulate_formatted_result(result=Solution.orm(session))
 
