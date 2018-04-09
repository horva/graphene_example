import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from models import *
from database import db_session


class Person(SQLAlchemyObjectType):
    class Meta:
        model = PersonModel
        interfaces = (graphene.relay.Node, )


class Article(SQLAlchemyObjectType):
    class Meta:
        model = ArticleModel
        interfaces = (graphene.relay.Node, )


class Query(graphene.ObjectType):
    node = graphene.relay.Node.Field()
    person = graphene.Field(Person, uuid=graphene.Int())
    persons = graphene.List(Person)

    def resolve_person(self, info, **args):
        query = Person.get_query(info)
        uuid = args.get('uuid')
        return query.get(uuid)

    def resolve_persons(self, info):
        query = Person.get_query(info)
        return query.all()


class CreatePerson(graphene.Mutation):
    class Arguments:
        name = graphene.String()
        age = graphene.Int()

    ok = graphene.Boolean()
    person = graphene.Field(lambda: Person)

    def mutate(self, info, name, age):
        p = PersonModel(name=name, age=age)
        db_session.add(p)
        db_session.commit()
        return CreatePerson(
            person=Person(name=p.name, age=p.age, uuid=p.uuid),
            ok=True
        )


class DeletePerson(graphene.Mutation):
    class Arguments:
        uuid = graphene.Int()

    ok = graphene.Boolean()
    person = graphene.Field(lambda: Person)

    def mutate(self, info, uuid):
        p = Person.get_query(info).get(uuid)
        db_session.delete(p)
        db_session.commit()
        return DeletePerson(
            person=Person(name=p.name, age=p.age, uuid=p.uuid),
            ok=True
        )


class Mutation(graphene.ObjectType):
    create_person = CreatePerson.Field()
    delete_person = DeletePerson.Field()


schema = graphene.Schema(query=Query, mutation=Mutation, types=[Person])
