# Artstractaguiar
#### Video Demo: https://youtu.be/cnMrpCFWxPg
#### Description:
Artstractaguiar is an e-commerce platform that sells abstract artworks generated randomly by the platform's algorithms. Users can browse a curated collection of unique artworks, register, and login in order to select their favorites and purchase prints.

## Table of Contents
- [Why the name](#name)
- [Features](#features)
- [Installation](#installation)
- [Requirements](#requirements)
- [Monetization Strategy](#monetization)
- [Technology Stack](#technology)

### Why the name
The name comes from Abstract Art, from there comes the Artstract, Art from itself, and Stract from abstract, taking the ab and changing it to art. Aguiar is because of my name, reflecting the founder's identity!

### Features

- Homepage Showcase: The homepage features a selection of abstract artworks generated randomly by the platform's algorithms. In it you see the artwork with a title, the price and a button to add to favorites and another to add to the cart.

- Favorites Showcase: In the favorites section, users can view all artworks marked as favorites, accompanied by their specifications. They have the options to remove from the favorites section or add artworks to the cart, providing a personalized art selection experience.

- Cart Showcase: In the cart, you see all the artworks you added to your cart, and below them you have their title, a button to remove from your cart, and at the end of all artworks, information on how to proceed with the payment and checkout.

- Register/Login: Users can register with a unique username, email, and password to access personalized features such as storing favorites and cart items. The login system ensures data security and a customized experience.

- Approve artwork: The administrator has exclusive access to validate artworks through the dedicated route. They can generate new artworks, set titles, prices, and accept or reject the pieces. The approved artworks are displayed for all users.

- Generate artwork: The algorithm randomly selects dimensions and shapes for artworks, including triangles, rectangles, circles, and ellipses. Points are chosen within the dimensions, connected, and given random RGB color values, the background color is also a random RGB color value.

- Database: I created a database to store the user properties and hashed their password for security, to store the artwork properties like status (if they have or have not been yet approved), to store each user's favorites, and also carts.

- FAQ: Created a Frequently Asked Questions page where you click the question in order to see the answer; there is a little arrow pointing down when the answer is hidden and pointing up when the answer is shown for an easier-to-use interface.

- Directions: Also created a Directions page for the user to know the location and different ways to contact us.

- Statics: Took a lot of care of the statics, making a personal logo for the homepage redirect and personalized icons for the favorites and cart pages. I made sure to work on the CSS style to make the web application user-friendly and welcome to look at; at least in my opinion, all the pages, including the logins, are well designed. I used a white and grayscale palette for the styling because I wanted the artworks to shine; the webpage shouldn't take attention from the beautiful abstract artworks.

- Login and admin required: The favorites and cart pages need login to be presented, but instead of just showing unauthorized, we redirect the user to register himself. Something similar happens when they try and access validate_artwork, something only I have access to.

- Details: Every aspect of Artstractaguiar reflects a commitment to excellence at the minutest level. From hover animations to color-coordinated footers, the platform's design elements are thoughtfully curated to provide a visually cohesive and user-friendly experience.

### Installation
No installation is required.

### Requirements
Flask==3.0.3
Flask_Login==0.6.3
numpy==1.26.4
Pillow==10.3.0
Werkzeug==3.0.3

## Monetization Strategy
Artstractaguiar generates revenue through the sale of prints of algorithmically generated abstract artworks. This approach aligns with the platform's core concept of offering unique and random artworks to art enthusiasts.

## Technology Stack
Frontend: HTML, CSS, JavaScript
Backend: Python (Flask for server-side logic)
Database: SQL (SQLite3 for storing user data and artwork information)
