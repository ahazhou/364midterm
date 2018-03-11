##TODO:
- **File has all setup (app.config, import, code to run) and properly runs**
- **Add navigation to base.html with links to every other viewable page**
- **Make sure all the templates in the application inherit (using template inheritance with **extends**) from base.html and include at least one additional **'block'****
- **Include at least 2(texthome.html) => 1 more template '.html' files that are not provided**
- **Have at least one additional template with a Jinja template for loop and another template with a Jinja template conditional (could be same or different templates)**
- **404 error handling and template**
- **At least 1 REST API request based on data submitted in a WTForm**
- **At least 1 not provided WTForm that sends a GET request to a **NEW** page**
- **At least 1 not provided WTForm that sends a POST request to the **SAME** page**
- **At least 1 custom validator for a field in a WTForm**
- **At least 2 additional model classes**
- **Have 1 one:many relationship between 2 of your models**
- **Successfully save data to each table**
- **Successfully query data from each of your models**
- **Query data using an **.all()** method in at least 1 view function and send the results of that query to a template**
- **Include at least 1 use of **redirect** (probs happens in view function where data is posted)**
- **Include at least 1 **url_for** (where you render a form)**
- **Have at least 3 view functions not included in the code**
- **Include an additional model class (to have 4 total) with at least 3 columns. Save data to it and query data from it; use the data you query in a view-function, which should have the data show up (or the result of the request made with the data show up)**
- **Write code in your file to allow a user submit duplicate data to a form, but will not save duplicate data (like the user should not be able to submit the same exact tweet)**
- **Bold completed tasks in this document**
- **Include list of all routes that exist int eh app and the names of templates each one should render such as /form => form.html or /form/<artist_name> => artist_links.html in this document**
- Contain at least 1 line of description of what your app is about or should do in this document

###ROUTES###
/ => base.html
/names => name_example.html
/login => login.html
/mainroute => texthome.html
/swearcheck => swearcheck.html
/insult => uniqueInsult.html
/* => 404.html

###APP DESCRIPTION###
This application is a very crude application in the sense that it is not for the faint of heart. Besides the original two pages, this application takes in your username and saves insults you generate toward another person. But not just any insult since they are creative. Also, this app allows the user the chance to check text for any swear words that might exist when typing difficult and annoying texts, informing the user of the presence of any bad words with a censored alternative. Everything that the user enters is saved. Except for the words "fuck you" when checking for text because this specific string is geared toward me, the developer, and since it is crude and not cordial, the program will not track it. Users are ID specific and another user with the same ID cannot exist.