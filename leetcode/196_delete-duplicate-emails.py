"""
https://leetcode.cn/problems/delete-duplicate-emails/description/

表: Person

+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| id          | int     |
| email       | varchar |
+-------------+---------+
id 是该表的主键列(具有唯一值的列)。
该表的每一行包含一封电子邮件。电子邮件将不包含大写字母。



编写解决方案 删除 所有重复的电子邮件，只保留一个具有最小 id 的唯一电子邮件。

（对于 SQL 用户，请注意你应该编写一个 DELETE 语句而不是 SELECT 语句。）

（对于 Pandas 用户，请注意你应该直接修改 Person 表。）

运行脚本后，显示的答案是 Person 表。驱动程序将首先编译并运行您的代码片段，然后再显示 Person 表。Person 表的最终顺序 无关紧要 。

返回结果格式如下示例所示。



示例 1:

输入:
Person 表:
+----+------------------+
| id | email            |
+----+------------------+
| 1  | john@example.com |
| 2  | bob@example.com  |
| 3  | john@example.com |
+----+------------------+
输出:
+----+------------------+
| id | email            |
+----+------------------+
| 1  | john@example.com |
| 2  | bob@example.com  |
+----+------------------+
解释: john@example.com重复两次。我们保留最小的Id = 1。

"""

from sqlalchemy import (
    String,
    select,
    delete,
    text,
    func,
    ChunkedIteratorResult,
)
from sqlalchemy.orm import Session, Mapped, aliased, mapped_column
from db import Base, engine
from utils import print_tabulate_formatted_result, insert_data_and_commit


class Person(Base):
    __tablename__ = "person"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255))


Base.metadata.create_all(engine)


class Solution:
    def sql(self, session: Session) -> ChunkedIteratorResult:
        # MySQL： delete p1 from person as p1 join person as p2 where p1.email = p2.email and p1.id > p2.id
        # SQLite 不支持 delete p1 的写法
        sql = """
            delete from person
            where id in (
                select p1.id
                from person as p1
                join person as p2 on p1.email = p2.email and p1.id > p2.id
            )
        """
        session.execute(text(sql))
        session.commit()

        result = session.execute(select(Person.id, Person.email))
        return result

    def orm(self, session: Session) -> ChunkedIteratorResult:
        p1 = aliased(Person)
        p2 = aliased(Person)

        stmt = delete(Person).where(
            Person.id.in_( 
                select(p1.id).join(p2, (p1.email == p2.email) & (p1.id > p2.id))
            )
        )
        session.execute(stmt)
        session.commit()

        result = session.execute(select(Person.id, Person.email))
        return result


if __name__ == "__main__":
    with Session(engine) as session:
        persons = [
            {"email": "john@example.com"},
            {"email": "bob@example.com"},
            {"email": "john@example.com"},
        ]

        insert_data_and_commit(persons, Person, session)
        print_tabulate_formatted_result(result=Solution().orm(session))
