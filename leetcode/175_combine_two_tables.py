"""
https://leetcode.cn/problems/combine-two-tables/description/

表: Person

+-------------+---------+
| 列名         | 类型     |
+-------------+---------+
| PersonId    | int     |
| FirstName   | varchar |
| LastName    | varchar |
+-------------+---------+
personId 是该表的主键（具有唯一值的列）。
该表包含一些人的 ID 和他们的姓和名的信息。



表: Address

+-------------+---------+
| 列名         | 类型    |
+-------------+---------+
| AddressId   | int     |
| PersonId    | int     |
| City        | varchar |
| State       | varchar |
+-------------+---------+
addressId 是该表的主键（具有唯一值的列）。
该表的每一行都包含一个 ID = PersonId 的人的城市和州的信息。



编写解决方案，报告 Person 表中每个人的姓、名、城市和州。如果 personId 的地址不在 Address 表中，则报告为 null 。

以 任意顺序 返回结果表。

结果格式如下所示。



示例 1:

输入:
Person表:
+----------+----------+-----------+
| personId | lastName | firstName |
+----------+----------+-----------+
| 1        | Wang     | Allen     |
| 2        | Alice    | Bob       |
+----------+----------+-----------+
Address表:
+-----------+----------+---------------+------------+
| addressId | personId | city          | state      |
+-----------+----------+---------------+------------+
| 1         | 2        | New York City | New York   |
| 2         | 3        | Leetcode      | California |
+-----------+----------+---------------+------------+
输出:
+-----------+----------+---------------+----------+
| firstName | lastName | city          | state    |
+-----------+----------+---------------+----------+
| Allen     | Wang     | Null          | Null     |
| Bob       | Alice    | New York City | New York |
+-----------+----------+---------------+----------+
解释:
地址表中没有 personId = 1 的地址，所以它们的城市和州返回 null。
addressId = 1 包含了 personId = 2 的地址信息。

"""

from sqlalchemy import String, Integer, select, text, ChunkedIteratorResult
from sqlalchemy.orm import Session, Mapped, mapped_column
from db import Base, engine
from utils import print_tabulate_formatted_result


class Person(Base):
    __tablename__ = "person"

    personId: Mapped[int] = mapped_column(primary_key=True)
    lastName: Mapped[str] = mapped_column(String(255))
    firstName: Mapped[str] = mapped_column(String(255))


class Address(Base):
    __tablename__ = "address"

    addressId: Mapped[int] = mapped_column(primary_key=True)
    personId: Mapped[int] = mapped_column(Integer)
    city: Mapped[str] = mapped_column(String(255))
    state: Mapped[str] = mapped_column(String(255))


Base.metadata.create_all(engine)


class Solution:

    def sql(self, session: Session) -> ChunkedIteratorResult:
        result = session.execute(
            text(
                "select p.firstName, p.lastName, a.city, a.state from person p left join address a on p.personId = a.personId"
            )
        )
        return result

    def orm(self, session: Session) -> ChunkedIteratorResult:
        stmt = (
            select(Person.firstName, Person.lastName, Address.city, Address.state)
            .select_from(Person)  # 指定查询的主表
            .outerjoin(
                Address, Person.personId == Address.personId
            )  # 指定副表和连接条件
        )

        result = session.execute(stmt)
        return result


if __name__ == "__main__":
    with Session(engine) as session:
        persons = [
            {"lastName": "Wang", "firstName": "Allen"},
            {"lastName": "Alice", "firstName": "Bob"},
        ]

        addresses = [
            {"personId": 2, "city": "New York City", "state": "New York"},
            {"personId": 3, "city": "Leetcode", "state": "California"},
        ]

        for i in range(len(persons)):
            person = Person(**persons[i])
            session.add(person)

        for i in range(len(addresses)):
            address = Address(**addresses[i])
            session.add(address)

        session.commit()

        print_tabulate_formatted_result(result=Solution().orm(session))

        # 操作 result
        # result = Solution().orm(session)
        # for row in result:
        #     print(row.firstName, row.lastName, row.city, row.state)
