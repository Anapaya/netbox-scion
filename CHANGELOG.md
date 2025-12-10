# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.4.0] - 2025-12-10

### Added
- Complete NetBox SCION plugin for managing SCION network infrastructure
- Three core models: Organizations, ISD-ASes, and SCION Link Assignments
- Organization management with ISD-AS relationships and auto-deletion of child ISD-ASes
- ISD-AS management with appliance tracking
- SCION Link Assignment management with peer relationships
- Status field for SCION Link Assignments (Reserved, Active, Planned) with color-coded badges
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
- Auto-select functionality for appliance field when editing SCION Link Assignments
