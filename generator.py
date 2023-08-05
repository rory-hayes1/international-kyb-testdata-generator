import json
import random
import string
from faker import Faker

class TemplateGenerator:
    def __init__(self, iso_code):
        self.fake = Faker()
        self.iso_code = iso_code.upper()
        self.entity_id_counter = 1

    def generate_entity_id(self):
        entity_id = f"{self.entity_id_counter:012d}"
        self.entity_id_counter += 1
        return "00000000-0000-0000-0000-" + entity_id


    def generate_template(self, num_linked_individuals, num_linked_organizations):
        template = {
            "requestId": self.fake.uuid4(),
            "createdAt": self.fake.iso8601(tzinfo=None),
            "details": {
                "addresses": [
                    {
                        "country": self.iso_code,
                        "longForm": self.fake.address(),
                        "postalCode": self.fake.postcode(),
                        "town": self.fake.city(),
                        "unstructuredLongForm": self.fake.street_address()
                    }
                ],
                "industryCodes": [
                    {
                        "code": self.fake.random_int(1000, 9999),
                        "description": self.fake.catch_phrase()
                    }
                ],
                "organizationName": self.fake.company(),
                "organizationStatus": "active",
                "organizationType": {
                    "code": self.fake.random_element(["ltd", "plc", "llp", "other"])
                },
                "registrationDetails": [
                    {
                        "foundationDate": self.fake.date(pattern="%Y-%m-%d"),
                        "registeredDate": self.fake.date(pattern="%Y-%m-%d"),
                        "registeredName": self.fake.company(),
                        "registeredStatus": "active",
                        "registrationNumber": self.fake.random_number(9, True),
                        "registryDescription": self.fake.catch_phrase()
                    }
                ]
            },
            "entityId": self.generate_entity_id(),
            "jusridcitionalInformation": {
                "personsOfSignificantControl": self.generate_persons_of_significant_control(num_linked_individuals),
                "linkedOrganizations": self.generate_linked_organizations(num_linked_organizations)
            },
            "linkedIndividuals": self.generate_linked_individuals(num_linked_individuals),
            "officeholders": [
                {
                    "entityId": self.generate_entity_id(),
                    "entityType": "INDIVIDUAL",
                    "officeholderTypeDescription": self.fake.random_element(["Director", "CEO", "CFO", "Secretary"])
                }
            ],
            "shareCapital": [
                {
                    "shareCount": self.fake.random_int(100, 99999)
                }
            ],
            "shareholders": self.generate_shareholders(num_linked_individuals, num_linked_organizations)
        }
        return template

    def generate_persons_of_significant_control(self, num_linked_individuals):
        persons_of_significant_control = []
        for i in range(1, num_linked_individuals + 1):
            person = {
                "addresses": [
                    {
                        "unstructuredLongForm": self.fake.street_address() + ", " + self.fake.city() + ", " + self.fake.country()
                    }
                ],
                "ceasedOn": self.fake.date(pattern="%Y-%m-%d"),
                "countryOfResidence": self.fake.country(),
                "dateOfBirth": self.fake.date(pattern="%Y-%m-%d"),
                "kind": "individual-person-with-significant-control",
                "name": self.fake.name(),
                "nationality": self.fake.country(),
                "natureOfControl": self.fake.random_elements(elements=("ownership-of-shares-25-to-50-percent",
                                                                       "voting-rights-25-to-50-percent",
                                                                       "ownership-of-shares-75-to-100-percent",
                                                                       "voting-rights-75-to-100-percent",
                                                                       "right-to-appoint-and-remove-directors"),
                                                              unique=True, length=random.randint(1, 5)),
                "notifiedOn": self.fake.date(pattern="%Y-%m-%d")
            }
            persons_of_significant_control.append(person)
        return persons_of_significant_control

    def generate_linked_organizations(self, num_linked_organizations):
        linked_organizations = {}
        for i in range(1, num_linked_organizations + 1):
            linked_organization = {
                "details": {
                    "organizationName": self.fake.company()
                },
                "entityId": self.generate_entity_id(),
                "entityType": "ORGANIZATION"
            }
            linked_organizations[linked_organization["entityId"]] = linked_organization
        return linked_organizations

    def generate_linked_individuals(self, num_linked_individuals):
        linked_individuals = {}
        for i in range(1, num_linked_individuals + 1):
            linked_individual = {
                "addresses": [
                    {
                        "postalCode": self.fake.postcode(),
                        "unstructuredLongForm": self.fake.street_address() + ", " + self.fake.city()
                    }
                ],
                "dateOfBirth": self.fake.date(pattern="%Y-%m-%d"),
                "entityId": self.generate_entity_id(),
                "entityType": "INDIVIDUAL",
                "name": self.fake.name(),
                "nationality": self.fake.country()
            }
            linked_individuals[linked_individual["entityId"]] = linked_individual
        return linked_individuals

    def generate_shareholders(self, num_linked_individuals, num_linked_organizations):
        shareholders = []
        total_percentage = 100
        num_linked_entities = num_linked_individuals + num_linked_organizations
        for i in range(1, num_linked_entities + 1):
            if i < num_linked_individuals + 1:
                entity_type = "INDIVIDUAL"
                entity_id = self.get_entity_id(i)
                name = self.fake.name()
                percentage_held = round(random.uniform(0, total_percentage), 2)
                total_percentage -= percentage_held
                shareholder = {
                    "currency": self.fake.currency_code(),
                    "entityId": entity_id,
                    "entityType": entity_type,
                    "nominalValue": self.fake.random_number(2, True),
                    "percentageHeld": percentage_held,
                    "sharesHeld": self.fake.random_int(1, 100),
                    "shareholderType": self.fake.random_element(["Company", "Individual"]),
                    "type": self.fake.random_element(["ORDINARY", "PREFERRED"])
                }
                if entity_type == "INDIVIDUAL":
                    shareholder["name"] = name
            else:
                entity_type = "ORGANIZATION"
                entity_id = self.get_entity_id(i)
                shareholder = {
                    "currency": self.fake.currency_code(),
                    "entityId": entity_id,
                    "entityType": entity_type,
                    "nominalValue": self.fake.random_number(2, True),
                    "percentageHeld": round(total_percentage, 2),
                    "sharesHeld": self.fake.random_int(1, 100),
                    "shareholderType": self.fake.random_element(["Company", "Individual"]),
                    "type": self.fake.random_element(["ORDINARY", "PREFERRED"])
                }
            shareholders.append(shareholder)
        return shareholders

    def get_entity_id(self, index):
        return f"{index:012d}"
