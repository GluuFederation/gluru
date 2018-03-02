# Gluru
Gluru is a free open source helpdesk ticketing system and knowledge base that is forked from the [Gluu customer and community support portal](https://support.gluu.org). 

Gluru is designed to leverage SuiteCRM for high level business logic, for instance, which users are associated with customer organizations, which "plan" or "product" is the user entitled to, etc. Gluru also uses [oxd](https://oxd.gluu.org) to support external authentication at any standard OpenID Provider, like the [Gluu Server](https://gluu.org) (our core free open source product!). 

### Setup development environment

The following apps are required for gluu support portal:
- Python 2.7.6
- Python Pip
- MySql 5.6
- Redis Server 2.10

### Virtual environment
Install `virtualenv` and `autoenv` modules first to setup a virtual environment:
```
sudo pip install virtualenv
sudo pip install autoenv
```

Then install the required modules:
```
cd <Gluru>
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```
### Other dependencies of gluru

- Update .env file according to your credentials.
- Integrate your SuiteCRM with gluru.
- For more information review crm_interface.py in connectors app.
- We have four roles of users: user, named, staff and partner.
- We have four support_plans "Basic, Standard, Premium and Enterprise" integrated with CRM, so you can setup CRM accordingly.

### Database migration

```
source .env
python manage.py makemigrations
python manage.py migrate
```
### Start the app

```
python manage.py runserver
```
App will be available at:
http://127.0.0.1:8000


### Application structure
  - Apps
      - alerts
      - connectors
      - profiles
      - search
      - tickets
  - Resources
      - static - static files css, js etc
      - templates - html templates
      - uploads - media files from interface uploads
  - Logs
      - logging data from connectors

### Alerts
   - application to send various alerts based on user/staff actions
   - emails templates are stored in database
   - tracking sent emails

### Connectors
   - Gluru uses [oxd](https://oxd.gluu.org) to support user authentication at an externa OpenID Provider (OP), like the [Gluu Server](https://gluu.org/) or Google. 
   - Register New user in Gluu IDP
   - Update user in Gluu IDP
   - Connector file crm_interface.py needs to be updated to communicate with CRM.

### Profiles
   - custom user profile
   - login base on IDP server using python-social-auth with a custom connector
   - each profile is sync, with CRM, at login
   - dashboard for tickets management
   - multiple users levels: basic, named, staff, partner

### Search
   - search using Haystack and Xapian

### Tickets
   - tickets, answer CRUD

### Note
   - This application is adjusted as per Gluu requirements so please adjust html and email templates accordingly.
   - This application is confirmed to work the [Gluu IDP](https://gluu.org/) or Google for authentication.
   - This application is designed to leverage SuiteCRM for business logic.
