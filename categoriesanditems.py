from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Categories, Items

engine = create_engine('sqlite:///itemCatelog.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# Ctaegory for Fashion
category1 = Categories(name="Fashion")

session.add(category1)
session.commit()

item1 = Items(name="Lakme EyeLiner", description="Blck Smooth Slim Fit TIP Eyeliner.",
                     category=category1)
session.add(item1)
session.commit()

item2 = Items(name="Lakme Kajal", description="Ultimate Kajal dgeproof, super long wear, moisturising ceramides.",
                     category=category1)
session.add(item2)
session.commit()

item3 = Items(name="L'oreal Paris Cocealer", description="Good blended concealer according to one's skin tone.",
                     category=category1)
session.add(item3)
session.commit()

item4 = Items(name="Lakme Lipstic", description="A longwearing matte lipstick that gives you Hi-Definition and intense color in one stroke.",
                     category=category1)
session.add(item4)
session.commit()

item5 = Items(name="Lakme Toner", description="Removes impurities, refreshes skin, tightens pores.",
                     category=category1)
session.add(item5)
session.commit()

# Ctaegory for Blogs
category2 = Categories(name="Blogs")

session.add(category2)
session.commit()

item1 = Items(name="ScoopWhoop", description="A blog which contain information in different section such as Humour, Travel, News etc.",
                     category=category2)

session.add(item1)
session.commit()


item2 = Items(name='''Thought Catelog", description="An online magazine which provide answers for any life question
              such as relationship, self-confidence from naive and as well as experienced writers.''',
                     category=category2)

session.add(item2)
session.commit()

# Ctaegory for Books
category3 = Categories(name="Books")

session.add(category3)
session.commit()

item1 = Items(name="Alchemist", description="Paulo Coelho.",
                     category=category3)

session.add(item1)
session.commit()


item2 = Items(name="Life is what you make it", description="Preeti Shenoy.",
                     category=category3)

session.add(item2)
session.commit()

item3 = Items(name="Lean In", description="Sheryl Sandberg.",
                     category=category3)
session.add(item3)
session.commit()

item4 = Items(name="The Low Land", description="Jhumpa Lehri.",
                     category=category3)
session.add(item4)
session.commit()

item5 = Items(name="Stay Foolish Stay Hungry", description="Rashmi Bansal.",
                     category=category3)
session.add(item5)
session.commit()

# Ctaegory for Acoustic
category4 = Categories(name="Acoustic")

session.add(category4)
session.commit()

item1 = Items(name="Guitar", description="Paulo Coelho.",
                     category=category4)

session.add(item1)
session.commit()


item2 = Items(name="Keyboard", description="Preeti Shenoy.",
                     category=category4)

session.add(item2)
session.commit()

item3 = Items(name="Flute", description="Sheryl Sandberg.",
                     category=category4)
session.add(item3)
session.commit()

item4 = Items(name="Violin", description="Jhumpa Lehri.",
                     category=category4)
session.add(item4)
session.commit()

item5 = Items(name="Trumpet", description="Rashmi Bansal.",
                     category=category4)
session.add(item5)
session.commit()

print "added items!"
