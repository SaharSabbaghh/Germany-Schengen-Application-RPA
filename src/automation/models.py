"""
Auto-generated Pydantic models for VIDEX form validation.
Generated from scraped form schema.
"""

from typing import Optional, Literal
from pydantic import BaseModel, Field


class Section0PersonalData(BaseModel):
    """Fields from: Personal Data"""

    antragsteller_familienname: Optional[str] = Field(None, description="Family name", max_length=40)
    antragsteller_geburtsname: Optional[str] = Field(None, description="Name at birth", max_length=40)
    antragsteller_vorname: Optional[str] = Field(None, description="First name(s)", max_length=55)
    antragsteller_geburtsdatum: Optional[str] = Field(None, description="Date of birth (dd.mm.yyyy)", max_length=5000)
    antragsteller_geburtsort: Optional[str] = Field(None, description="Place of birth", max_length=35)
    rechtAufFreizuegigkeit: Optional[bool] = Field(None, description="Yes")
    antragsteller_personendaten_berufdaten_firmenname: Optional[str] = Field(None, description="Company name and telephone number (for students name and telephone number of educational establishment)", max_length=50)
    antragsteller_personendaten_berufdaten_strasse: Optional[str] = Field(None, description="Street", max_length=50)
    antragsteller_personendaten_berufdaten_hausnummer: Optional[str] = Field(None, description="House number", max_length=10)
    antragsteller_personendaten_berufdaten_sonstigeAdressangaben: Optional[str] = Field(None, description="Other address information", max_length=50)
    antragsteller_personendaten_berufdaten_plz: Optional[str] = Field(None, description="Postal code", max_length=15)
    antragsteller_personendaten_berufdaten_ort: Optional[str] = Field(None, description="Town/city", max_length=50)
    antragsteller_personendaten_staendigeAnschrift_strasse: Optional[str] = Field(None, description="Street", max_length=50)
    antragsteller_personendaten_staendigeAnschrift_hausnummer: Optional[str] = Field(None, description="House number", max_length=10)
    antragsteller_personendaten_staendigeAnschrift_sonstigeAdressangaben: Optional[str] = Field(None, description="Other address information", max_length=50)
    antragsteller_personendaten_staendigeAnschrift_plz: Optional[str] = Field(None, description="Postal code", max_length=15)
    antragsteller_personendaten_staendigeAnschrift_ort: Optional[str] = Field(None, description="Town/city", max_length=50)
    antragsteller_personendaten_staendigeAnschrift_kontaktdaten_telefon: Optional[str] = Field(None, description="Telephone/mobile number", max_length=30)
    antragsteller_personendaten_staendigeAnschrift_kontaktdaten_email: Optional[str] = Field(None, description="Email", max_length=80)
    antragsteller_aufenthaltsberechtigung: Optional[bool] = Field(None, description="Is your residence in a country other than that of your current nationality?")
    antragsteller_pass_passnummer: Optional[str] = Field(None, description="Travel document number", max_length=20)
    antragsteller_nationaleIdentNr: Optional[str] = Field(None, description="National identity number, where applicable", max_length=50)
    antragsteller_pass_gueltigVon: Optional[str] = Field(None, description="Date of issue (dd.mm.yyyy)", max_length=5000)
    antragsteller_pass_gueltigBis: Optional[str] = Field(None, description="Valid until (dd.mm.yyyy)", max_length=5000)
    antragsteller_pass_ausgestelltVon: Optional[str] = Field(None, description="Issued by", max_length=50)
    antragsteller_pass_ausgestelltIn: Optional[str] = Field(None, description="Issued in", max_length=50)
    antragsteller_biometrie_fingerabdrueckeErfassungsDatum_vorhanden: Optional[bool] = Field(None, description="Yes")
    reisedaten_letzteVisumStickernummer: Optional[bool] = Field(None, description="Visa sticker number, if known")
    reisedaten_angegebenerReisezweck: Optional[str] = Field(None, description="Other (please specify)", max_length=250)
    reisedaten_weitereInformationen: Optional[str] = Field(None, description="Further information on the purpose of the stay", max_length=250)
    visumdaten_gueltigkeit_von: Optional[str] = Field(None, description="Intended date of arrival for the first intended stay in the Schengen area", max_length=5000)
    visumdaten_gueltigkeit_bisGenau_value: Optional[str] = Field(None, description="Intended date of departure from the Schengen area after the first intended stay", max_length=5000)
    antragsteller_einreisegenehmigung_einreisegenehmigungsNr: Optional[str] = Field(None, description="Entry permit number", max_length=50)
    antragsteller_einreisegenehmigung_ausgestelltVon: Optional[str] = Field(None, description="Issued by", max_length=50)
    antragsteller_einreisegenehmigung_gueltigVon: Optional[str] = Field(None, description="Valid from (dd.mm.yyyy)", max_length=5000)
    antragsteller_einreisegenehmigung_gueltigBis: Optional[str] = Field(None, description="Valid until (dd.mm.yyyy)", max_length=5000)
    referenz_ansprechpartner_familienname: Optional[str] = Field(None, description="Family name", max_length=5000)
    referenz_ansprechpartner_vorname: Optional[str] = Field(None, description="First name(s)", max_length=5000)
    referenz_ansprechpartner_geburtsdatum: Optional[str] = Field(None, description="Date of birth (dd.mm.yyyy)", max_length=5000)
    referenz_ansprechpartner_geburtsort: Optional[str] = Field(None, description="Place of birth", max_length=5000)
    referenz_ansprechpartner_anschrift_strasse: Optional[str] = Field(None, description="Street", max_length=5000)
    referenz_ansprechpartner_anschrift_hausnummer: Optional[str] = Field(None, description="House number", max_length=5000)
    referenz_ansprechpartner_anschrift_plz: Optional[str] = Field(None, description="Postal code", max_length=5000)
    referenz_ansprechpartner_anschrift_ort: Optional[str] = Field(None, description="Town/city", max_length=5000)
    referenz_ansprechpartner_kontaktdaten_telefon: Optional[str] = Field(None, description="Telephone/mobile number", max_length=5000)
    referenz_ansprechpartner_kontaktdaten_email: Optional[str] = Field(None, description="Email", max_length=5000)
    referenz_ansprechpartner_abweichendeSchreibweiseNachname: Optional[str] = Field(None, description="Alternative spelling - surname(s)", max_length=5000)
    referenz_ansprechpartner_abweichendeSchreibweiseVorname: Optional[str] = Field(None, description="Alternative spelling - first name(s)", max_length=5000)
    referenz_ansprechpartner_andereNamen: Optional[str] = Field(None, description="Other names", max_length=5000)
    referenz_ansprechpartner_fruehereNamen: Optional[str] = Field(None, description="Previous names", max_length=5000)
    reisedaten_reisekostenUebernahme_antragsteller: Optional[bool] = Field(None, description="the applicant him/herself")
    reisedaten_reisekostenUebernahme_dritte: Optional[bool] = Field(None, description="a third party (host, company, organisation), please specify")
    reisedaten_lebensunterhalt_bar: Optional[bool] = Field(None, description="Cash")
    reisedaten_lebensunterhalt_reiseschecks: Optional[bool] = Field(None, description="Traveller's cheques")
    reisedaten_lebensunterhalt_kreditkarten: Optional[bool] = Field(None, description="Credit cards")
    reisedaten_lebensunterhalt_unterkunft: Optional[bool] = Field(None, description="Accommodation paid in advance")
    reisedaten_lebensunterhalt_vollstaendigeKostenuebernahme: Optional[bool] = Field(None, description="Assumption of all expenses during the stay")
    reisedaten_lebensunterhalt_befoerderung: Optional[bool] = Field(None, description="Transport paid in advance")
    reisedaten_lebensunterhalt_sonstiges: Optional[bool] = Field(None, description="Other (please specify)")
    antragsteller_geburtsland: Optional[str] = Field(None, description="Country of birth")
    antragsteller_geschlecht: Optional[Literal["Male", "Female", "Unspecified"]] = Field(None, description="Sex")
    antragsteller_familienstand: Optional[Literal["Single", "Married", "Civil partnership", "Separated", "Divorced", "Widowed", "Unknown"]] = Field(None, description="Marital status")
    antragsteller_staatsangehoerigkeitListe_0_: Optional[str] = Field(None, description="Current nationality")
    antragsteller_staatsangehoerigkeitBeiGeburtListe_0_: Optional[str] = Field(None, description="Original nationality")
    antragsteller_personendaten_berufdaten_berufAuswahl: Optional[str] = Field(None, description="Current occupation")
    antragsteller_personendaten_berufdaten_land: Optional[str] = Field(None, description="Country")
    antragsteller_personendaten_staendigeAnschrift_land: Optional[str] = Field(None, description="Country")
    antragsteller_pass_passArt: Optional[str] = Field(None, description="Type of travel document")
    antragsteller_pass_ausstellenderStaat: Optional[str] = Field(None, description="Issuing state")
    reisedaten_aufenthaltszweckListe_0_: Optional[str] = Field(None, description="Purpose(s) of the journey")
    reisedaten_ersteinreiseStaat: Optional[str] = Field(None, description="Member State of first entry")
    reisedaten_hauptzielListe_0_: Optional[str] = Field(None, description="Main travel destination(s)")
    visumdaten_anzahlEinreisen: Optional[Literal["Single entry", "Two entries", "Multiple entries"]] = Field(None, description="Number of entries requested")
    antragsteller_einreisegenehmigung_artDerEinreisegenehmigungAuswahl: Optional[Literal["residence permit", "re-entry visa", "resident alien card", "Other"]] = Field(None, description="Type of entry permit")
    antragsteller_einreisegenehmigung_endzielStaat: Optional[str] = Field(None, description="Final country of destination")
    referenz_referenzArt: Optional[Literal["No reference person", "Inviting person", "Inviting organisation/company", "Hotel", "Accredited diplomat", "EU citizen", "Householder", "Rental of private accommodation (by commercial lessor)", "Rental of private accommodation (by private individual)"]] = Field(None, description="Type of reference")
    referenz_ansprechpartner_geschlecht: Optional[Literal["Male", "Female", "Unspecified"]] = Field(None, description="Sex")
    referenz_ansprechpartner_staatsangehoerigkeit: Optional[str] = Field(None, description="Nationality")
    referenz_ansprechpartner_anschrift_land: Optional[str] = Field(None, description="Country")


class Section1ContactDetails(BaseModel):
    """Fields from: Contact Details"""

    pass


class Section2Documents(BaseModel):
    """Fields from: Documents"""

    pass


class Section3TravelData(BaseModel):
    """Fields from: Travel Data"""

    pass


class Section4Reference(BaseModel):
    """Fields from: Reference"""

    pass


class Section5CostCoverage(BaseModel):
    """Fields from: Cost Coverage"""

    pass


class VidexApplication(BaseModel):
    """Complete VIDEX visa application data."""

    section0_personal_data: Section0PersonalData
    section1_contact_details: Section1ContactDetails
    section2_documents: Section2Documents
    section3_travel_data: Section3TravelData
    section4_reference: Section4Reference
    section5_cost_coverage: Section5CostCoverage
