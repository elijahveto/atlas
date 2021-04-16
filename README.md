# atlas
A django based web app that allows smaller companies to share knowledge and best practices among employees. 

Deployed with Heroku: https://lit-waters-05102.herokuapp.com/

--------



Functionalities by database: 


Users
- must belong to a company
- one user per company is superuser and can delete/ edit sections (where all content is stored) by accessing certain sites)

Company
- unique company names allowed
- user must input a company he belongs to, company will be created if company not registered yet 

Sections
- contain the posts and serve as topic buckets for users to navigate

Posts
- contain title and text 
- use tinymce rich text editor 
- can be edited and deleted only by creator

Comments
- per post
- can be edited and deleted only by creator

Likes 
- can be given to posts and comments
- one per user and item


-------------

Initializaion 

- requires setting a manager group > run:

from django.contrib.auth.models import Group

Group.objects.create(name='manager')


// design
homepage uses artwork by Niels Vadot (https://codepen.io/ninivert/pen/ZpEQBR)
