# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.3.2] - 2025-12-03

### Fixed
- Added missing `@register_search` decorator to `SCIONLinkAssignmentIndex` class to enable global search functionality for SCION Link Assignments

## [1.3.1] - 2025-11-26

### Added
- Clickable ISD-ASes section header on Organization detail page that filters the ISD-AS list

### Changed
- Renamed "Full ISD-AS Path" label to "ISD-AS" in SCION Link Assignment detail page
- Made ISD-AS value clickable in Related Information section

### Fixed
- Appliance field now correctly auto-selects existing value when editing a SCION Link Assignment
- JavaScript initialization and value restoration now use polling-based ready checks instead of fixed timeouts for better reliability across different system speeds
- Peer field unique constraint now allows multiple links with empty peer field for the same ISD-AS

## [1.3.0] - 2025-10-01

### Added
- Comments field for Organization, ISD-AS, and SCION Link Assignment models
- Peer column to SCION Link Assignments table in ISD-AS detail view
- Clickable "SCION Link Assignments" section header on ISD-AS detail page
- Local and peer underlay fields for SCION Link Assignments with IP:port validation
- Status field for SCION Link Assignments (Reserved, Active, Planned)
- Color-coded badges for Status and Relationship fields

### Changed
- Renamed `zendesk_ticket` field to generic `ticket`
- Ticket field now accepts URLs and renders them as clickable hyperlinks
- Made `peer_name` and `peer` fields optional for SCION Link Assignments

### Fixed
- Comments fields now exposed in API serializers
- Status, underlay, and comments fields now displayed on SCION Link Assignment form
- Plugin changelog pages now display correctly

### Removed
- Customer ID field from SCION Link Assignments

## [1.2.0] - 2025-09-09

### Added
- Peer field for SCION Link Assignments with unique constraint per ISD-AS
- Peer field validation with format help text
- Auto-deletion of ISD-ASes when parent organization is deleted

### Changed
- **BREAKING:** Renamed `customer_name` field to `peer_name`
- **BREAKING:** Renamed `cores` field to `appliances` in ISD-AS model
- **BREAKING:** Removed `appliance_type` field - appliances are now generic
- Updated all UI labels from "Customer Name" to "Peer Name" and "Core" to "Appliance"

### Fixed
- Database schema inconsistencies
- Field reference errors throughout codebase
- Migration issues with unique constraints

## [1.1.2] - 2025-09-05

### Fixed
- Missing filter buttons on all list pages
- NoReverseMatch errors when organization field is null
- Corrupted detail templates
- ListView template references
- Null value handling in templates
- Interface ID column now clickable in SCION Link Assignment table

### Changed
- Improved table rendering with null organization fields
- Enhanced navigation between detail pages
- Updated package naming to be PEP 625 compliant

## [1.1.1] - 2025-09-05

### Changed
- Updated installation documentation and deployment instructions

## [1.1.0] - 2025-09-05

### Added
- Appliance Type field for ISD-AS (CORE and EDGE options)
- Advanced filtering interface for all list pages
- Dedicated Appliances management section in ISD-AS detail pages

### Changed
- Renamed "Core Nodes" to "Appliances" throughout the UI

### Fixed
- Filter sidebar display on all list pages
- Appliance dropdown loading when ISD-AS is selected

## [1.0.0] - 2025-09-03

### Added
- Complete NetBox SCION plugin with Organizations, ISD-ASes, and SCION Link Assignments
- Dynamic appliance dropdown based on ISD-AS selection
- Relationship types (PARENT/CHILD/CORE) for link classification
- Full REST API with CRUD operations, filtering, and pagination
- Export functionality (CSV/Excel)
- Audit logging and change tracking
- PyPI package distribution

### Fixed
- Form validation and error messages
- Dropdown functionality and user experience

## [0.1.0] - 2025-08-31

### Added
- Initial plugin release with core functionality
- Zendesk ticket integration with clickable links
- Basic database models and API structure

