Overview: ECommerce site for Smart Home Company(Listen Hear). Built for use by home builders and designers to add smart home packages to home building plans before mortage / financing finalized.

Stack: Django Cookie Cutter, Html, CSS, JS, Bootstrap5, Docker

Styling:
    - Primary: #417ce3
    - Secondary: #fbd01c
    - Compliment: #2f2e2e

Data models: Smart home company can add categories, sub categories to build 'packages'. Building tiered packages for the categories / subs. Think good, better, best. Home builder will be able to add several packages based by category / sub category to total an estimate of costs. Generating a form / packages list with both parties via email. Salespersons follows up off platform 


Builders account details: 
Company Name 
Contact Person(s)
Email
Phone
Bio
Website
Avatar


PackageTemplate: 
Name
Category
Category - > SubCategory
Picture for Category, SubCategory, Package
Description / Includes 
Estimated Price Low
Estimated Price High 
Price Notes (Asterisks)
Install Phases Required (Allow multiple)
Requires 'Install Phase' (optional)
Grouping Coupon (If product added, save X if other package added)
Utility Incentive (Boolean)


Quote Request: 
Generate form to share with client they are designing / building for. Simple with listen hear logo attached. Emails to builder and smart home company. Includes packages purchased, contact details, estimation to hear from listen hear. 

Smart Home Workflow: 
Able to create catalogs, sub catalogs. Tier pricing packages including multiple items within catalogs / sub catalogs. 

Define packages by various inputs such as sq foot, estimated pricing, room count, product count etc. Easy add via django admin.

Builder Workflow: Visit site installer selets interested packages, add packages to cart, see checkout page, checkout. checkout is just generated pdf via email, listen hear will follow up depending on work case. automated generated form. 

UI/UX: Clean experience, allowing buildings / designers to sit down withe the home builder, or even share site to home builder, get packages, share receipt with constructer / designer. 


