import datetime, xmlrpclib


wp_url = "http://students.thelycaeum.in/blog/xmlrpc.php"
wp_username = "beingshahul"
wp_password = "n9EDcoT9JuSs"
wp_blogid = ""

status_draft = 0
status_published = 1

server = xmlrpclib.ServerProxy(wp_url)

title = "Instantaneous post"
content = "Testing from publish application."
categories = ["Uncategorized"]
tags = ["sometag", "othertag"]
data = {'title': title, 'description': content, 'categories': categories, 'mt_keywords': tags}

post_id = server.metaWeblog.newPost(wp_blogid, wp_username, wp_password, data, status_published)
