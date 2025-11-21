# Listen Hear - Smart Home Package Estimator

## Project Overview
Simple e-commerce platform for Listen Hear to showcase smart home packages. Builders create accounts, select packages, and receive automated cost estimates via email. No payment processing - Listen Hear follows up offline.

## Technology Stack
- **Backend**: Django Cookie Cutter
- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5
- **Containerization**: Docker
- **Project Structure**: All apps in `listenhear/listen_hear/` root directory

## Design System

### Color Palette
- **Primary**: `#417ce3`
- **Secondary**: `#fbd01c`
- **Accent**: `#2f2e2e`

---

## Apps Structure
```
listenhear/listen_hear/
├── packages/          # Categories, SubCategories, PackageTemplates
├── accounts/          # Builder accounts (extends django-cookiecutter users)
├── cart/              # Shopping cart session management
└── estimates/         # Generated estimates (the "receipts")
```

### `packages/` - Product Catalog
**Models:**
- `Category` - Top-level grouping (e.g., "Audio", "Security", "Lighting")
- `SubCategory` - Nested under Category (e.g., "Whole Home Audio", "Outdoor Audio")
- `PackageTemplate` - The actual products (tiered: Good/Better/Best)
- `InstallPhase` - User-defined installation phase package is installed
- Not all packages require subcategory

**PackageTemplate Fields:**
```python
name = CharField
category = ForeignKey(Category)
subcategory = ForeignKey(SubCategory, blank=True) #not mandatory for package build
image = ImageField
description = TextField  # What's included
price_low = DecimalField  # Estimated range
price_high = DecimalField
price_notes = TextField  # Disclaimers/asterisks
install_phases = ManyToManyField('InstallPhase', blank=True)
requires_phase = ForeignKey('InstallPhase', blank=True, null=True)
bundle_discount_note = CharField(blank=True)  # "Save $X when combined with Y"
utility_incentive_eligible = BooleanField(default=False)
is_active = BooleanField(default=True)
created_at = DateTimeField(auto_now_add=True)
updated_at = DateTimeField(auto_now=True)
```

**InstallPhase Fields:**
```python
name = CharField  # e.g., "Pre-Wire", "Rough-In", "Finish"
description = TextField
order = IntegerField  # Display order
is_active = BooleanField(default=True)
```

**Category Fields:**
```python
name = CharField
image = ImageField(blank=True)
description = TextField(blank=True)
order = IntegerField  # Display order
is_active = BooleanField(default=True)
```

**SubCategory Fields:**
```python
name = CharField
category = ForeignKey(Category)
image = ImageField(blank=True)
description = TextField(blank=True)
order = IntegerField  # Display order
is_active = BooleanField(default=True)
```

### `accounts/` - Builder Management
Extends Django-Cookiecutter user model with:
```python
company_name = CharField
contact_person = CharField
phone = CharField
bio = TextField(blank=True)
website = URLField(blank=True)
avatar = ImageField(blank=True)
created_at = DateTimeField(auto_now_add=True)
updated_at = DateTimeField(auto_now=True)
```

### `cart/` - Session Management
Simple session-based cart (no database model needed until checkout)

**Session Structure:**
```python
request.session['cart'] = {
    'package_id_1': {'quantity': 1, 'name': '...', 'price_low': '...', 'price_high': '...'},
    'package_id_2': {'quantity': 1, 'name': '...', 'price_low': '...', 'price_high': '...'},
}
```

### `estimates/` - Generated Estimates
**Estimate Model:**
```python
estimate_number = CharField(unique=True)  # Auto-generated (e.g., EST-2024-001)
builder = ForeignKey(User)
client_name = CharField(blank=True)  # Homeowner name
client_email = EmailField(blank=True)
packages = ManyToManyField(PackageTemplate, through='EstimateItem')
total_low = DecimalField  # Sum of price_low
total_high = DecimalField  # Sum of price_high
notes = TextField(blank=True)
created_at = DateTimeField(auto_now_add=True)
updated_at = DateTimeField(auto_now=True)
status = CharField(choices=['pending', 'contacted', 'converted', 'archived'])
```

**EstimateItem Model (through table):**
```python
estimate = ForeignKey(Estimate)
package = ForeignKey(PackageTemplate)
price_low_snapshot = DecimalField  # Snapshot at time of estimate
price_high_snapshot = DecimalField
package_name_snapshot = CharField  # In case package is deleted/renamed
```

---

## User Flows

### Anonymous Browsing
1. Browse packages by category/subcategory
2. View package details (description, pricing, install phases, etc.)
3. Add packages to cart
4. View cart summary

### Checkout Flow (Account Required)
1. Click "Confirm Estimate" from cart
2. **If not logged in**: Redirect to login/register page
3. **If logged in**: Proceed to estimate form
5. Add optional notes
6. Submit estimate request
7. Receive branded PDF via email (Builder + Listen Hear copies)
8. Redirect to "Thank You" page with estimate summary

### Builder Dashboard
1. View past 'checkouts'
2. View estimate details
3. Edit builder details 

### Listen Hear Admin Workflow
1. Create/manage Categories & SubCategories
2. Build PackageTemplates (define all fields manually)
3. Define custom InstallPhases
4. View/manage submitted estimates
6. Export builder estimates to CSV/Excel

---

## Admin Permissions (django-admin)

### Roles:
- **Superadmin**: Full access to everything
- **Project Manager**: Create/edit Categories, SubCategories, Packages, InstallPhases
- **Sales Manager**: View all estimates, update status, export reports

---

## Key Features

✅ **No payment processing** - estimates only  
✅ **User-defined pricing** - all package prices set manually by admins  
✅ **Tiered packages** - Good/Better/Best naming convention  
✅ **Bundle hints** - Display "save x on utility,  
✅ **Open browsing** - account not required to add to cart and request estimates 
✅ **Email automation** - PDF receipt estimates generated and sent to builder + Listen Hear  
✅ **Mobile responsive** - Bootstrap 5  
✅ **Estimate history** - Builders can view past estimates

---

## Technical Implementation Notes

### Django Cookie Cutter Usage
- Use built-in user model as base for Builder accounts
- Leverage existing authentication system
- Use built-in email configuration
- Follow cookie-cutter app structure conventions

### Cart Implementation
- Session-based cart (no database until checkout)
- Store package IDs and snapshot data in session
- on checkout require business contact info / zip / details unless registered /authenticated user
- Clear cart after successful estimate submission

### PDF Generation
- Use `weasyprint` or `reportlab`
- Template includes:
  - Listen Hear branding/logo
  - Estimate number and construction date
  - Builder company info
  - Client info (if provided)
  - Line items (packages with price ranges)
  - Total estimate range
  - Notes/disclaimers
  - Install phases summary
  - Contact information for follow-up

### Email System
- Django's built-in email with HTML templates
- Recipients: Builder email + Listen Hear admin email
- Optional: CC client email if provided
- Attach PDF estimate
- Include plain text fallback

### URL Structure
```
/                              # Homepage (featured packages)
/packages/                     # All packages
/packages/category/<slug>/     # Packages by category
/packages/<slug>/              # Package detail
/cart/                         # View cart
/cart/add/<package_id>/        # Add to cart
/cart/remove/<package_id>/     # Remove from cart
/checkout/                     # Estimate request form (login required)
/estimates/                    # Builder estimate history
/estimates/<estimate_number>/  # Estimate detail
/accounts/register/            # Register
/accounts/login/               # Login
/accounts/dashboard/           # Builder dashboard
```

---

## UI/UX Goals

### Design Principles
- **Clean, minimal interface** - Focus on products, not clutter
- **Easy package comparison** - Side-by-side views of Good/Better/Best
- **Clear pricing transparency** - Always show price ranges
- **Mobile-responsive** - Bootstrap 5 responsive grid
- **Fast checkout flow** - Minimal form fields, require filling out contact info on checkout.

### Primary Use Case
Builder sits with homeowner to configure packages in real-time on tablet/laptop

### Secondary Use Case
Builder shares site link with homeowner for self-service browsing and estimate requests
