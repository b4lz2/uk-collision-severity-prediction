# Unit Mappings — `collisions` Table

This document records the unit-of-measurement annotations applied to the numeric attributes of the `collisions` table in DBRepo.

**Selection methodology:** SI Digital Framework was checked first, then OMG Commons. OMG Commons is a meta-ontology with no concrete unit instances, so unmapped attributes were assigned QUDT URIs (referenced by OMG Commons itself as the de-facto unit ontology).

| Column | Unit | Ontology | URI |
|---|---|---|---|
| `location_easting_osgr` | metre | SI Digital Framework | [https://si-digital-framework.org/SI/units/metre](https://si-digital-framework.org/SI/units/metre) |
| `location_northing_osgr` | metre | SI Digital Framework | [https://si-digital-framework.org/SI/units/metre](https://si-digital-framework.org/SI/units/metre) |
| `longitude` | degree | SI Digital Framework | [https://si-digital-framework.org/SI/units/degree](https://si-digital-framework.org/SI/units/degree) |
| `latitude` | degree | SI Digital Framework | [https://si-digital-framework.org/SI/units/degree](https://si-digital-framework.org/SI/units/degree) |
| `speed_limit` | mile per hour | QUDT | [https://qudt.org/vocab/unit/MI-PER-HR](https://qudt.org/vocab/unit/MI-PER-HR) |
| `collision_year` | year | QUDT | [https://qudt.org/vocab/unit/YR](https://qudt.org/vocab/unit/YR) |
| `number_of_vehicles` | number (count) | QUDT | [https://qudt.org/vocab/unit/NUM](https://qudt.org/vocab/unit/NUM) |
| `number_of_casualties` | number (count) | QUDT | [https://qudt.org/vocab/unit/NUM](https://qudt.org/vocab/unit/NUM) |
| `collision_adjusted_severity_serious` | fraction | QUDT | [https://qudt.org/vocab/unit/FRACTION](https://qudt.org/vocab/unit/FRACTION) |

## Justifications

### `location_easting_osgr`
British National Grid easting is expressed in metres, directly mappable to the SI base unit for length.

### `location_northing_osgr`
British National Grid northing in metres, SI base unit for length.

### `longitude`
WGS84 longitude is recorded in decimal degrees. SI explicitly lists degree as a non-SI unit accepted for use with the SI.

### `latitude`
WGS84 latitude in decimal degrees, see longitude.

### `speed_limit`
UK road speed limits are legally defined in miles per hour. SI does not include imperial units; OMG Commons is a meta-ontology with no concrete unit instances. QUDT, referenced by OMG Commons itself as the de-facto unit ontology, provides a stable URI for mph.

### `collision_year`
The SI base unit for time is the second; year is not part of SI. OMG Commons defines no specific unit instances. QUDT provides a curated URI for calendar year, suitable for annual aggregation.

### `number_of_vehicles`
Dimensionless count of vehicles per collision. SI represents dimensionless quantities as 'one' but does not publish a browseable URI for this concept. QUDT NUM provides a stable URI.

### `number_of_casualties`
Dimensionless count of casualties per collision, see number_of_vehicles.

### `collision_adjusted_severity_serious`
Probability value in [0, 1] indicating adjusted likelihood that a collision was of 'serious' severity. QUDT FRACTION captures both dimensionlessness and the 0-to-1 range characteristic of fractions.

