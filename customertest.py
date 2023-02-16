from model import Customer
import unittest

# sut = system under test

class CustomerTest(unittest.TestCase):
    def test_When_creating_person_then_name_and_personnumber_should_be_set(self):
        GivenName = "Stefan"
        NationalId = "19720803-0000"
        sut = Customer(GivenName,NationalId)
        self.assertEqual(GivenName, sut.Name)
        self.assertEqual(NationalId, sut.PersonNumber)        

class CustomerRegisterTest(unittest.TestCase):
    def test_When_fetching_person_correct_person_should_be_returned(self):     
        person1 = Customer("Stefan", "19720803-0000")
        person2 = Customer("Kalle", "19790101-0000")
        sut = Customer()
        sut.add(person1)
        sut.add(person2)
        result = sut.getPerson("19720803-0000")
        self.assertEqual(person1, result)

    # def test_When_fetching_person_and_person_does_not_exist_correct_errormessage_should_be_returned(self):    
    #     #arrange    
    #     person1 = Person("Stefan", "19720803-0000")
    #     person2 = Person("Kalle", "19790101-0000")
    #     sut = PersonRegister()
    #     sut.add(person1)
    #     sut.add(person2)
    #     #act
    #     result = sut.getPerson("19720803-1111")
    #     #assert
    #     self.assertEqual("Finns inte", result)


    def test_When_adding_person_and_person_already_exist_correct_errormessage_should_be_returned(self):    
        #arrange    
        person1 = Customer("Stefan", "19720803-0000")
        person2 = Customer("Kalle", "19720803-0000")
        sut = Customer()
        sut.add(person1)
        result = sut.add(person2)
        self.assertEqual("Duplicate key", result)

if __name__ == '__main__':
    unittest.main()