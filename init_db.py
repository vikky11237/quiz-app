from app import app, db
from models import Category, Question, User, QuizScore
from datetime import datetime

def init_db():
    with app.app_context():
        # Drop all tables first to ensure clean state
        db.drop_all()
        
        # Create all tables
        db.create_all()

        # Create categories
        categories = [
            Category(name='General Knowledge'),
            Category(name='Science'),
            Category(name='History'),
            Category(name='Geography'),
            Category(name='Technology'),
            Category(name='Sports')
        ]
        db.session.add_all(categories)
        db.session.commit()

        # Get category references
        general = Category.query.filter_by(name='General Knowledge').first()
        science = Category.query.filter_by(name='Science').first()
        history = Category.query.filter_by(name='History').first()
        geography = Category.query.filter_by(name='Geography').first()
        technology = Category.query.filter_by(name='Technology').first()
        sports = Category.query.filter_by(name='Sports').first()

        # Add sample questions
        questions = [
            # General Knowledge Questions
            Question(
                category=general,
                question_text='Which is the most spoken language in the world?',
                option_1='English',
                option_2='Spanish',
                option_3='Mandarin Chinese',
                option_4='Hindi',
                correct_answer='Mandarin Chinese'
            ),
            Question(
                category=general,
                question_text='What is the name of the biggest technology company in South Korea?',
                option_1='Sony',
                option_2='Samsung',
                option_3='LG',
                option_4='Hyundai',
                correct_answer='Samsung'
            ),
            Question(
                category=general,
                question_text='What is the name of the longest river in the world?',
                option_1='Amazon',
                option_2='Nile',
                option_3='Mississippi',
                option_4='Yangtze',
                correct_answer='Nile'
            ),

            # Science Questions
            Question(
                category=science,
                question_text='What is the hardest natural substance on Earth?',
                option_1='Gold',
                option_2='Iron',
                option_3='Diamond',
                option_4='Platinum',
                correct_answer='Diamond'
            ),
            Question(
                category=science,
                question_text='What is the chemical symbol for gold?',
                option_1='Ag',
                option_2='Au',
                option_3='Fe',
                option_4='Cu',
                correct_answer='Au'
            ),
            Question(
                category=science,
                question_text='Which planet is known as the Red Planet?',
                option_1='Venus',
                option_2='Jupiter',
                option_3='Mars',
                option_4='Saturn',
                correct_answer='Mars'
            ),

            # History Questions
            Question(
                category=history,
                question_text='In which year did World War II end?',
                option_1='1943',
                option_2='1944',
                option_3='1945',
                option_4='1946',
                correct_answer='1945'
            ),
            Question(
                category=history,
                question_text='Who was the first President of the United States?',
                option_1='Thomas Jefferson',
                option_2='George Washington',
                option_3='John Adams',
                option_4='Benjamin Franklin',
                correct_answer='George Washington'
            ),
            Question(
                category=history,
                question_text='Which ancient wonder of the world was located in Egypt?',
                option_1='Hanging Gardens',
                option_2='Colossus of Rhodes',
                option_3='Great Pyramid of Giza',
                option_4='Temple of Artemis',
                correct_answer='Great Pyramid of Giza'
            ),

            # Geography Questions
            Question(
                category=geography,
                question_text='What is the capital of Australia?',
                option_1='Sydney',
                option_2='Melbourne',
                option_3='Canberra',
                option_4='Perth',
                correct_answer='Canberra'
            ),
            Question(
                category=geography,
                question_text='Which is the smallest continent by land area?',
                option_1='Europe',
                option_2='Australia',
                option_3='Antarctica',
                option_4='South America',
                correct_answer='Australia'
            ),
            Question(
                category=geography,
                question_text='Which country has the most islands in the world?',
                option_1='Indonesia',
                option_2='Japan',
                option_3='Sweden',
                option_4='Philippines',
                correct_answer='Sweden'
            ),

            # Technology Questions
            Question(
                category=technology,
                question_text='Who is the co-founder of Microsoft Corporation?',
                option_1='Steve Jobs',
                option_2='Bill Gates',
                option_3='Mark Zuckerberg',
                option_4='Jeff Bezos',
                correct_answer='Bill Gates'
            ),
            Question(
                category=technology,
                question_text='What does "HTTP" stand for?',
                option_1='HyperText Transfer Protocol',
                option_2='High Transfer Text Protocol',
                option_3='HyperText Technical Program',
                option_4='High Technical Transfer Program',
                correct_answer='HyperText Transfer Protocol'
            ),
            Question(
                category=technology,
                question_text='In what year was the first iPhone released?',
                option_1='2005',
                option_2='2006',
                option_3='2007',
                option_4='2008',
                correct_answer='2007'
            ),

            # Sports Questions
            Question(
                category=sports,
                question_text='Which country won the FIFA World Cup 2022?',
                option_1='France',
                option_2='Brazil',
                option_3='Argentina',
                option_4='Germany',
                correct_answer='Argentina'
            ),
            Question(
                category=sports,
                question_text='How many players are there in a standard basketball team on court?',
                option_1='4',
                option_2='5',
                option_3='6',
                option_4='7',
                correct_answer='5'
            ),
            Question(
                category=sports,
                question_text='In which sport would you perform a slam dunk?',
                option_1='Football',
                option_2='Volleyball',
                option_3='Basketball',
                option_4='Tennis',
                correct_answer='Basketball'
            )
        ]

        db.session.add_all(questions)
        
        # Create admin user
        admin_user = User(
            username="admin",
            name="Admin User",
            is_admin=True
        )
        admin_user.set_password("admin123")
        db.session.add(admin_user)
        
        db.session.commit()
        print("Database initialized successfully with sample questions!")

if __name__ == '__main__':
    init_db() 