from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_Setup import Categories, Base, Items

engine = create_engine('sqlite:///shopdata.db')
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



category1 = Categories(name="Facewash", image="https://i.ytimg.com/vi/9gtMdYHiaio/maxresdefault.jpg")

session.add(category1)
session.commit()

item1 = Items(name="Garnier Mens Facewash", description = "Garnier Men's first Dual Texture face wash designed to remove dust & pollution and give fairer looking skin.'\n'Formula enriched with Salicylic Active and Vitamin C, known to exfoliate skin and reduce dullness respectively.'\n'Cleanses Skin Deeply, removing oil, dirt and pollution.'\n'Skin Looks More Even, radiant and feels fresh all day.", price = '180 Rs', image = "https://images-eu.ssl-images-amazon.com/images/I/41S29mghnIL._SY355_.jpg", seller_name = "rupali bindal", seller_address = "#238 vpo ratttewali, dist. barwala, Panchkula", seller_phoneno = "7082667891", categories = category1)
session.add(item1)
session.commit()

item2 = Items(name="Clean and Clear", description="Clean & Clear Foaming face wash is specially designed to cleanse thoroughly and remove excess oil.'\n'Recommended for: Those who want to prevent oily shine and pimples.", price = "110 Rs", image="https://images-na.ssl-images-amazon.com/images/I/31BwAWIl4jL.jpg", seller_name="rupali bindal",seller_address = "#238 vpo rattewali, dist. barwala, Panchkula", seller_phoneno = "7082667891", categories = category1)

session.add(item2)
session.commit()

item3 = Items(name="Himalya neem Facewash", description="Hydrates skin'\n'Removes impurities'/n'Cleanses face", price="117 Rs", image="https://images-na.ssl-images-amazon.com/images/I/716vG7Pw9pL._SL1500_.jpg", seller_name="rupali bindal",seller_address = "#238 vpo rattewali, dist. barwala, Panchkula", seller_phoneno = "7082667891", categories = category1)
session.add(item3)
session.commit()

item4 = Items(name="Nivea Mens Facewash", description="Cooling mud (natural charcoal) formula cleanses and removes excess oils and impurities deeply in pores'\n'Reduces dark spots due to dirt and brightens skin'\n'Refreshing and cool feeling on the skin", price="195 Rs", image="https://images-na.ssl-images-amazon.com/images/I/61xnX9xKwML._SL1100_.jpg", seller_name="rupali bindal",seller_address = "#238 vpo rattewali, dist. barwala, Panchkula", seller_phoneno = "7082667891", categories = category1)
session.add(item4)
session.commit()

category2 = Categories(name = "Kurkure", image="http://3.bp.blogspot.com/-okkBC_M9Ezw/Vk3DqS_Ra7I/AAAAAAAAACA/WLD7gELwb5w/s400/Kurkure%2BMasala%2BMunch.jpg")
session.add(category2)
session.commit()

item1 = Items(name="Kurkure-Masala Munch", description="Flavour: Masala Munch", price="10 Rs, 20 Rs", image="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcScb1q3jT3oje2XAFiFlQFQFKu6HgEVniE2Y5R_IKdVwg2U2iJ7", seller_name="Shubham", seller_address="#238 vpo rattewali, dist. barwala, Panchkula", seller_phoneno = "9996386154", categories = category2)
session.add(item1)
session.commit()

item2 = Items(name="Kurkure-Chilli Chataka", description="Flavour: Chilli Chataka", price="10 Rs, 20Rs", image="https://5.imimg.com/data5/YM/UU/M0Y-35438113/kurkure-chilli-chatka-500x500.jpg", seller_name="Shubham Gupta", seller_address="#238 vpo rattewali, dist. barwala, Panchkula", seller_phoneno="9996386154", categories=category2)
session.add(item2)
session.commit()

item3 = Items(name="Kurkure-Solid Masti", description="Flavour-Masala", price="10 Rs, 20Rs", image="http://www.grocerybazaar.in/wp-content/uploads/2017/08/Kurkure-Solid-Masti-Twisteez-Masala-40-Gm.jpg", seller_name="Shubham Gupta", seller_address="#238 vpo rattewali, dist. barwala, Panchkula", seller_phoneno="9996386154", categories=category2)
session.add(item3)
session.commit()

item4 = Items(name="Kurkure-PuffCorn", description="Flavour-Yummy Cheese", price="10 Rs, 20 Rs", image="https://images-na.ssl-images-amazon.com/images/I/81q5sKbW9WL._SX342_.jpg", seller_name="Shubham Gupta", seller_address="#238 vpo rattewali, dist. barwala, Panchkula", seller_phoneno="9996386154", categories=category2)
session.add(item4)
session.commit()

category3 = Categories(name = "Chips", image="https://rukminim1.flixcart.com/image/832/832/j5y7gcw0-1/chips/k/h/c/52-potato-chips-american-style-cream-onion-flavour-lay-s-original-imaewj5xfny4tvus.jpeg?q=70")
session.add(category3)
session.commit()

item1 = Items(name = "Lays - American Style Cream and Onion Flavour", description = "Flavour- American Style Cream and Onion Flavour", price = "10 Rs, 20 Rs", image="https://rukminim1.flixcart.com/image/832/832/j5y7gcw0-1/chips/k/h/c/52-potato-chips-american-style-cream-onion-flavour-lay-s-original-imaewj5xfny4tvus.jpeg?q=70", seller_name="Shubham Gupta", seller_address="#238 vpo rattewali, dist. barwala, Panchkula", seller_phoneno="9996386154", categories=category3)
session.add(item1)
session.commit()

item2 = Items(name="Lays - India's Masala Magic Flavour", description="Flavour: India's Masala Magic", price='10 Rs, 20 Rs', image="https://1.bp.blogspot.com/-7MbO_bZNQU8/VwWdJ67_6OI/AAAAAAAAOUc/oDj4kZvSDYYoYDp4mBSyN73WsRPYHgPaQ/s1600/lays.jpg", seller_name="Shubham Gupta", seller_address="#238 vpo rattewali, dist. barwala, Panchkula", seller_phoneno="9996386154", categories=category3)
session.add(item2)
session.commit()

item3 = Items(name="Lays - MAXX",description="Flavour: MAXX hot and sour punch", price= "30 Rs", image="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQhXAgGcrxkx6I6jXZUV_A-Uue2RE0un4_sCdJavWLJG1K0J_vq3w", seller_name="Shubham Gupta", seller_address="#238 vpo rattewali, dist. barwala, Panchkula", seller_phoneno="9996386154", categories=category3)
session.add(item3)
session.commit()

category4 = Categories(name ="Cold Drinks", image="https://4.imimg.com/data4/FD/WQ/IMOB-48314342/beverages-website-500x500.png")
session.add(category4)
session.commit()

item1 = Items(name="Pepsi", description="Pepsi is a carbonated soft drink produced and manufactured by PepsiCo. This Flavour is cola.", price="Rs 15 for 300ml '\n'Rs 35 for 600ml'\n'Rs 60 for 1.25L'\n'Rs80 for 2L", image="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRqYkqkpynqd8FnC5SXGhLCvJ8uEN10J473VDa0xM-B2dO9r_V3", seller_name="Shubham Gupta", seller_address="#238 vpo rattewali, dist. barwala, Panchkula", seller_phoneno="9996386154", categories=category4)
session.add(item1)
session.commit()

item2 = Items(name="Mirinda", description="Mirinda is a carbonated soft drink owned by PepsiCo. This Flavour is orange.", price="Rs 15 for 300ml '\n'Rs 35 for 600ml'\n'Rs 60 for 1.25L'\n'Rs80 for 2L", image="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTNfiv8jZvpU7XgmK1l0b1STwmIZIgGBbq_6V1ZJhrp7VJmNih6", seller_name="Shubham Gupta", seller_address="#238 vpo rattewali, dist. barwala, Panchkula", seller_phoneno="9996386154", categories=category4)
session.add(item2)
session.commit()

item3 = Items(name="Limca", description="Limca is a lemon and lime flavoured carbonated soft drink made primarily in India.", price="Rs 15 for 300ml '\n'Rs 35 for 600ml'\n'Rs 60 for 1.25L'\n'Rs80 for 2L", image="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTNfiv8jZvpU7XgmK1l0b1STwmIZIgGBbq_6V1ZJhrp7VJmNih6", seller_name="Shubham Gupta", seller_address="#238 vpo rattewali, dist. barwala, Panchkula", seller_phoneno="9996386154", categories=category4)
session.add(item3)
session.commit()

item4 = Items(name="Mountain Dew", description="Mountain Dew (stylized as Mtn Dew) is a carbonated soft drink brand produced and owned by PepsiCo.", price="Rs 15 for 300ml '\n'Rs 35 for 600ml'\n'Rs 60 for 1.25L'\n'Rs80 for 2L", image="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR98L9zmPVKiOsbHX4ovc9pYPvZyEJZUZepfjQX-HHm2BGOdZOD", seller_name="Shubham Gupta", seller_address="#238 vpo rattewali, dist. barwala, Panchkula", seller_phoneno="9996386154", categories=category4)
session.add(item4)
session.commit()

item5 = Items(name="Fanta", description="Fanta originated as a cola substitute as a result of difficulties importing Coca-Cola.", price="Rs 15 for 300ml '\n'Rs 35 for 600ml'\n'Rs 60 for 1.25L'\n'Rs80 for 2L", image="https://s3-ap-southeast-1.amazonaws.com/media.redmart.com/newmedia/1600x/i/m/8888002086503_0082_1453179774812.jpg", seller_name="Shubham Gupta", seller_address="#238 vpo rattewali, dist. barwala, Panchkula", seller_phoneno="9996386154", categories=category4)
session.add(item5)
session.commit()

category5 = Categories(name="Milk Products", image="http://www.vitaindia.org.in/product/vita_dahi_l.jpg")
session.add(category5)
session.commit()

item1 = Items(name="Dahi", description="Vita dahi", price="Rs 18 for 200ml'\n'Rs 35 for 450gms", image ="http://www.vitaindia.org.in/product/vita_dahi_l.jpg", seller_name="Shubham Gupta", seller_address="#238 vpo rattewali, dist. barwala, Panchkula", seller_phoneno="9996386154", categories=category5)
session.add(item1)
session.commit()

item2 = Items(name="Amul Moti Milk", description="Milk", price="Rs 26 for 500ml", image="https://leafyexpress.com/wp-content/uploads/2014/12/Amul-Moti-Fresh-Toned-Milk-500ml.jpg", seller_name="Shubham Gupta", seller_address="#238 vpo rattewali, dist. barwala, Panchkula", seller_phoneno="9996386154", categories=category5)
session.add(item2)
session.commit()

item3 = Items(name="Vita Lassi", description="Lassi", price="Rs 25 for 1L", image="http://www.vitaindia.org.in/product/vita_lassi_l.jpg", seller_name="Shubham Gupta", seller_address="#238 vpo rattewali, dist. barwala, Panchkula", seller_phoneno="9996386154", categories=category5)
session.add(item3)
session.commit()

item4 = Items(name="Amul Makhan", description="Makhan", price="Rs 42", image="http://www.futurekirana.com/image/cache/data/image%20new-15-01-13/Amul-Butter-100-g-500x500.jpg", seller_name="Shubham Gupta", seller_address="#238 vpo rattewali, dist. barwala, Panchkula", seller_phoneno="9996386154", categories=category5)
session.add(item4)
session.commit()

item5 = Items(name="Vita Paneer", description="Paneer", price="Rs 60 for 200g", image="https://i.ytimg.com/vi/Q38XFIWciS8/hqdefault.jpg", seller_name="Shubham Gupta", seller_address="#238 vpo rattewali, dist. barwala, Panchkula", seller_phoneno="9996386154", categories=category5)
session.add(item5)
session.commit()

print "added menu items!"