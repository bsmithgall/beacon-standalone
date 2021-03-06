# -*- coding: utf-8 -*-

import datetime

import factory
from factory.alchemy import SQLAlchemyModelFactory

from beacon.database import db
from beacon.models.users import User, Role, Department

from beacon.models.opportunities import (
    Opportunity, RequiredBidDocument, OpportunityDocument, Category,
    Vendor, OpportunityType
)
from beacon.jobs.job_base import JobStatus

class BaseFactory(SQLAlchemyModelFactory):
    class Meta:
        abstract = True
        sqlalchemy_session = db.session

class RoleFactory(BaseFactory):
    id = factory.Sequence(lambda n: n)
    name = factory.Sequence(lambda n: '{}'.format(n))

    class Meta:
        model = Role

class DepartmentFactory(BaseFactory):
    id = factory.Sequence(lambda n: n)
    name = factory.Sequence(lambda n: 'department{}'.format(n))

    class Meta:
        model = Department

class UserFactory(BaseFactory):
    id = factory.Sequence(lambda n: n + 100)
    email = factory.Sequence(lambda n: '{}'.format(n))
    created_at = factory.Sequence(lambda n: datetime.datetime.now())
    first_name = factory.Sequence(lambda n: '{}'.format(n))
    last_name = factory.Sequence(lambda n: '{}'.format(n))
    department = factory.SubFactory(DepartmentFactory)
    active = factory.Sequence(lambda n: True)
    role = factory.SubFactory(RoleFactory)

    class Meta:
        model = User

class CategoryFactory(BaseFactory):
    id = factory.Sequence(lambda n: n)
    category_friendly_name = 'i am friendly!'

    class Meta:
        model = Category

class OpportunityFactory(BaseFactory):
    id = factory.Sequence(lambda n: n + 100)
    department = factory.SubFactory(DepartmentFactory)
    contact = factory.SubFactory(UserFactory)
    created_by = factory.SubFactory(UserFactory)
    title = 'Default'

    @factory.post_generation
    def categories(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for category in extracted:
                self.categories.add(category)

    class Meta:
        model = Opportunity

class OpportunityTypeFactory(BaseFactory):
    id = factory.Sequence(lambda n: n + 100)

    class Meta:
        model = OpportunityType

class VendorFactory(BaseFactory):
    id = factory.Sequence(lambda n: n + 100)
    email = factory.Sequence(lambda n: '{}@foo.com'.format(n))
    business_name = factory.Sequence(lambda n: '{}'.format(n))

    @factory.post_generation
    def categories(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for category in extracted:
                self.categories.add(category)

    class Meta:
        model = Vendor

class RequiredBidDocumentFactory(BaseFactory):
    display_name = 'name'
    description = 'description'

    class Meta:
        model = RequiredBidDocument

class OpportunityDocumentFactory(BaseFactory):
    class Meta:
        model = OpportunityDocument

class JobStatusFactory(BaseFactory):
    class Meta:
        model = JobStatus
