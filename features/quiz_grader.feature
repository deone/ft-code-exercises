Feature: setup system

  Scenario: create teacher
    Given we have a teacher
    And a classroom
    When teacher is created
    Then teacher should have a name
    And a classroom

Feature: setup system
  
  Scenario: create student
    Given we have a student
    And a classroom
    When student is created
    Then student should have a name
    And a classroom

Feature: quiz creation
  
  Scenario: create quiz
    Given we have questions
    And answers
    When quiz is created
    Then quiz should have questions
    And answers

Feature: quiz assignment
  
  Scenario: assign quiz
    Given we have a teacher
    And a student
    And a quiz
    When quiz is assigned
    Then student should have a quiz

Feature: do quiz
  
  Scenario: solve question
    Given we have a student
    And a quiz
    And a question
    When question is solved
    Then question should have an answer

Feature: quiz grading
  
  Scenario: grade quiz
    Given we have a student
    And a completed quiz
    When quiz is graded
    Then we should have grade entry