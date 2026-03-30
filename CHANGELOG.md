# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.4.1] - 2026-03-30

### Added
- PEER relationship type for SCION Links with orange color-coded badge
- Export button on Organization detail page (ZIP with organization, ISD-ASes, and SCION Links CSVs)
- Edit button for each individual link on the SCION Links block in the ISD-AS detail page

### Changed
- Renamed "Core Node" label to "Appliance" on SCION Link detail page
- Relationship badges now display in uppercase (CORE, PARENT, CHILD, PEER)
- "Create & Add Another" on SCION Link form now preserves the selected ISD-AS value

### Fixed
- CSV export encoding: added UTF-8 BOM for proper special character display in Excel
- CSV export of ISD-AS list no longer includes HTML links for organization name
- CSV export of SCION Links no longer includes HTML span badges for relationship and status

## [1.4.0] - 2025-12-10

### Added
- Complete NetBox SCION plugin for managing SCION network infrastructure
- Three core models: Organizations, ISD-ASes, and SCION Links
- Organization management with ISD-AS relationships and auto-deletion of child ISD-ASes
- ISD-AS management with appliance tracking
- SCION Link management with peer relationships
- Status field for SCION Links (Reserved, Active, Planned) with color-coded badges
- Local and peer underlay fields with IP:port validation
- Peer field with unique constraint per ISD-AS and format validation
- Comments fields for all main models
- Ticket field for tracking external tickets with clickable URL support
- Relationship types (PARENT/CHILD/CORE) for link classification with color-coded badges
- Full REST API with CRUD operations, filtering, and pagination
- Advanced filtering interface for all list pages
- Global search functionality for all models
- Export functionality (CSV/Excel) for all list views
- Audit logging and change tracking
- Dynamic appliance dropdown based on ISD-AS selection
- Clickable section headers for improved navigation between detail pages
- Enhanced table rendering with proper null value handling
- Form validation with reliable JavaScript initialization using polling-based ready checks
- Auto-select functionality for appliance field when editing SCION Links
