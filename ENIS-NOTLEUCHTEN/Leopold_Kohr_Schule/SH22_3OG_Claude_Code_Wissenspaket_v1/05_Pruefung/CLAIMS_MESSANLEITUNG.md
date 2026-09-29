# Messanleitung der 104 Soll-Aussagen

Die 32 Fälle verwenden 88 verschiedene Feldnamen. Diese Datei erklärt jede Aussage und ihre Auswertung. Boolesche Negativbehauptungen sind nur nach tatsächlicher Prüfung false; ein fehlendes Ergebnis ist unbekannt/ungeprüft. Die Messanleitung bestimmt keine willkürlichen universellen Toleranzen.

## `wall_body_blocks_floor`

Die ganze belegte Wandbreite ist aus dem freien Boden ausgespart.

**Auswertung:** Wandkörper und Freifläche räumlich vergleichen, nicht nur die Achslinie.

**Sollfälle:** SH22-W01 = `true`

## `layer_gaps_are_walkway`

Schichtzwischenräume der Außenwand wurden als Gehflächen behandelt.

**Auswertung:** Freiflächen im belegten Wandpaket und ihre Quellzuordnung untersuchen.

**Sollfälle:** SH22-W01 = `false`

## `material_claim_without_source`

Ein Wandmaterial wurde ohne passenden Materialbeleg behauptet.

**Auswertung:** Materialattribute und ihre konkreten Belege prüfen; Layerfarbe allein genügt nicht.

**Sollfälle:** SH22-W01 = `false`

## `wall_separate_from_furniture`

Die bauliche Wand und die davorstehende Einrichtung sind verschiedene Objekte.

**Auswertung:** Objekt- und Grenzbezüge hinter der Möblierung verfolgen.

**Sollfälle:** SH22-W02 = `true`

## `portal_in_solid_partition`

In der geschlossenen Trennwand wurde eine unbewiesene Passage erzeugt.

**Auswertung:** Alle lokalen Portale gegen den vollständigen Wandkörper prüfen.

**Sollfälle:** SH22-W02 = `false`

## `ceiling_material_used_as_wall_material`

Eine D:-Angabe wurde als Materialbeweis der Wand verwendet.

**Auswertung:** Attributprovenienz von D:, W: und Materialfeld vergleichen.

**Sollfälle:** SH22-W02 = `false`

## `thin_partitions_block_crossing`

Auch die dünnen WC-Kabinenplatten verhindern seitlichen Durchtritt.

**Auswertung:** Sperrflächen und Graphkanten an den konkreten Trennplatten prüfen.

**Sollfälle:** SH22-W03 = `true`

## `cubicles_are_subspaces`

Kabinen werden als Unterstruktur des WC-Raums geführt.

**Auswertung:** Elternraum-/Teilraumrelation und Zugänge prüfen.

**Sollfälle:** SH22-W03 = `true`

## `arc_is_solid_obstacle`

Der Schwenkbogen oder sein ganzer Sektor wurde als massive Sperrfläche benutzt.

**Auswertung:** Bogenherkunft und daraus abgeleitete Hindernisgeometrie nachverfolgen.

**Sollfälle:** SH22-W03 = `false`, SH22-D01 = `false`

## `leaf_and_arc_separate`

Türblatt und Bewegungsbogen sind semantisch getrennt.

**Auswertung:** Beide Ursprungsgeometrien müssen mit unterschiedlicher Funktion auffindbar sein.

**Sollfälle:** SH22-D01 = `true`

## `portal_at_wall_opening`

Die Verbindung liegt in der tatsächlichen Wandöffnung.

**Auswertung:** Portalgeometrie, Laibungen und beide Nachbarflächen räumlich abgleichen.

**Sollfälle:** SH22-D01 = `true`

## `live_door_state`

Tatsächlicher gegenwärtiger Öffnungs-/Verriegelungszustand der Tür.

**Auswertung:** Die gezeichnete Stellung ist kein Live-Sensor; ohne Betriebsquelle unknown.

**Sollfälle:** SH22-D01 = `"unknown"`

## `jambs_bound_portal`

Die Laibungen begrenzen die lichte Portalöffnung.

**Auswertung:** Enden der Portalgeometrie mit beiden Original-Laibungen abgleichen.

**Sollfälle:** SH22-D02 = `true`

## `graph_edge_through_solid_jamb`

Eine Wegkante schneidet die feste Laibung.

**Auswertung:** Schnittprüfung im lokalisierten Türbereich durchführen.

**Sollfälle:** SH22-D02 = `false`

## `leaf_state_is_conditional`

Die Benutzbarkeit berücksichtigt einen veränderlichen Türblattzustand.

**Auswertung:** Portalbedingung und Bewegungs-/Blattmodell getrennt nachweisen.

**Sollfälle:** SH22-D02 = `true`

## `one_opening_two_leaves`

Zwei Flügel gehören zu einer gemeinsamen Öffnung.

**Auswertung:** Gemeinsame Laibungsöffnung sowie zwei Drehpunkte/Blätter zuordnen.

**Sollfälle:** SH22-D03 = `true`

## `two_arcs_are_two_rooms`

Zwei Bögen wurden als zwei eigene Räume gezählt.

**Auswertung:** Prüfen, ob Bogenkonturen produktive Raumgrenzen erzeugen.

**Sollfälle:** SH22-D03 = `false`

## `clear_width_counted_twice`

Die gemeinsame lichte Breite wurde pro Flügel nochmals addiert.

**Auswertung:** Portalmaß und Flügelmaße mit Provenienz vergleichen.

**Sollfälle:** SH22-D03 = `false`

## `classification`

Fachliche Klasse des lokalisierten Beispielobjekts.

**Auswertung:** Aus Engine-Klasse auf den vereinbarten Fallwert abbilden, nicht aus der Beispiel-ID ableiten.

**Sollfälle:** SH22-F01 = `"window"`, SH22-M03 = `"wardrobe_furniture"`, SH22-T01 = `"stair"`, SH22-T03 = `"stair"`, SH22-T04 = `"stair"`, SH22-R04 = `"storage_room"`

## `normal_walking_portal`

Es existiert eine gewöhnliche Gehpassage durch dieses Element.

**Auswertung:** Bodenanschluss, Brüstung und tatsächlich erzeugte Graphkante prüfen.

**Sollfälle:** SH22-F01 = `false`, SH22-F02 = `false`

## `parapet_reference`

Höhenbezug der im Beispiel ausgewerteten FPH-Angabe.

**Auswertung:** Originaltext und Attributbezug prüfen; FPH ü. FBOK ist nicht RPH ü. RDOK.

**Sollfälle:** SH22-F01 = `"FBOK"`

## `glazing_layers`

Genau bestimmter Glasschichtenaufbau.

**Auswertung:** Ohne zugehöriges Detail unknown; Fensterklasse allein reicht nicht.

**Sollfälle:** SH22-F01 = `"unknown"`

## `frame_and_glazing_zone_separate`

Rahmen-/Profilzone und vermutete Verglasungszone bleiben unterscheidbar.

**Auswertung:** Merkmalsrollen und Unsicherheit einzelner Linien prüfen.

**Sollfälle:** SH22-F02 = `true`

## `exact_glass_panes`

Genau identifizierte einzelne Glasscheiben.

**Auswertung:** Nicht jede parallele Linie als Scheibe deklarieren; ohne Detail unknown.

**Sollfälle:** SH22-F02 = `"unknown"`

## `tables_chairs_are_furniture`

Tisch- und Sitzsymbole werden als Einrichtung gelesen.

**Auswertung:** Wiederholung, Kontur und Raumbezug anhand tatsächlicher Objektrollen prüfen.

**Sollfälle:** SH22-M01 = `true`

## `free_gaps_preserved`

Belegte freie Zwischenräume der konkreten Möbelgruppe bleiben erhalten.

**Auswertung:** Objektweise Hindernisflächen mit den freien Zwischenräumen vergleichen.

**Sollfälle:** SH22-M01 = `true`, SH22-M03 = `true`

## `furniture_creates_room_boundaries`

Möbelkonturen erzeugen neue bauliche Raumgrenzen.

**Auswertung:** Herkunft produktiver Raumgrenzen kontrollieren.

**Sollfälle:** SH22-M01 = `false`

## `cabinet_and_wall_separate`

Schrankreihe und Wand dahinter sind unterschiedliche Objekte.

**Auswertung:** Durchgehende Wandanschlüsse hinter lokalen Einrichtungsfeldern prüfen.

**Sollfälle:** SH22-M02 = `true`

## `cross_is_stair`

Diagonalkreuze in Schrankfeldern wurden als Treppe ausgelegt.

**Auswertung:** Klasse/Höhenrelation der gekreuzten Möbelzellen kontrollieren.

**Sollfälle:** SH22-M02 = `false`

## `cabinet_footprint_blocked`

Die belegte Schrankstellfläche wird aus dem freien Boden ausgespart.

**Auswertung:** Lokale Möbelfläche mit Freifläche vergleichen.

**Sollfälle:** SH22-M02 = `true`

## `height_transition_invented`

Aus der Garderobenmöblierung wurde ein unbelegter Höhenwechsel erzeugt.

**Auswertung:** Stair-/Level-Verbindungen in dieser Möbelgruppe prüfen.

**Sollfälle:** SH22-M03 = `false`

## `wc_and_basin_distinguished`

WC-Schüssel und Waschbecken sind als verschiedene Ausstattung erkannt.

**Auswertung:** Kontur, Aufstellung und lokale Sanitärrolle vergleichen.

**Sollfälle:** SH22-S01 = `true`

## `installation_strip_is_general_walkway`

Die rückwärtige Installationszone wurde als allgemeiner Gang freigegeben.

**Auswertung:** Boden-/Zugangsbelege und Verbindungen im Streifen prüfen.

**Sollfälle:** SH22-S01 = `false`

## `sanitary_is_room_wall`

Sanitärkonturen wurden zu baulichen Raumwänden.

**Auswertung:** Klassifikation und Raumgrenzen-Provenienz kontrollieren.

**Sollfälle:** SH22-S01 = `false`

## `room_labels_follow_leaders`

Ausgelagerte Raumtexte folgen ihren Zuordnungslinien.

**Auswertung:** Textanker über Bezugslinie bis zum tatsächlich zugeordneten Raum nachweisen.

**Sollfälle:** SH22-S02 = `true`

## `printer_room_separate_from_wc`

Druckerraum und WC bleiben getrennte Räume mit passender Nutzung.

**Auswertung:** Umfassung, eigene Türen und Textzuordnung prüfen.

**Sollfälle:** SH22-S02 = `true`

## `nearest_text_only_assignment`

Die Zuordnung stützt sich ausschließlich auf nächsten Textabstand.

**Auswertung:** Entscheidungsbelege prüfen; Nähe darf Kandidatensuche, nicht alleinige Begründung sein.

**Sollfälle:** SH22-S02 = `false`, SH22-R03 = `false`

## `kitchen_equipment_separate`

Küchengeräte/Einbauten sind von baulichen Grenzen getrennt.

**Auswertung:** Gerätefelder, Arbeitsflächen und Raumumfassung als verschiedene Rollen auswerten.

**Sollfälle:** SH22-M04 = `true`

## `basin_alone_causes_wc_classification`

Ein einzelnes Becken hat ohne weiteren Beleg eine WC-Raumklasse ausgelöst.

**Auswertung:** Funktionsklassifikation und die tatsächlich verwendeten Belege prüfen.

**Sollfälle:** SH22-M04 = `false`

## `room_function_uses_label`

Der passend zugeordnete Raumtext wird für die Nutzung ausgewertet.

**Auswertung:** Nutzungseigenschaft mit Raumstempel/Bezugslinie verknüpfen.

**Sollfälle:** SH22-M04 = `true`

## `treads_are_walls`

Stufenvorderkanten wurden als bauliche Wände behandelt.

**Auswertung:** Linienrollen und daraus abgeleitete Sperr-/Raumgrenzen prüfen.

**Sollfälle:** SH22-T01 = `false`, SH22-T03 = `false`

## `ascent_from_arrow_and_sequence`

Aufwärtsrichtung wird mit Pfeil und Stufenfolge gemeinsam begründet.

**Auswertung:** Pfeilanfang/-ende, Nummern, Folge und Podestbezug nachweisen.

**Sollfälle:** SH22-T01 = `true`

## `target_floor_without_height_evidence`

Ein Zielgeschoss wurde ohne passende Anschlusshöhen behauptet.

**Auswertung:** Ziel-ID und ihre vertikalen Belege prüfen.

**Sollfälle:** SH22-T01 = `false`, SH22-T02 = `false`

## `break_is_wall`

Das Treppenbruchzeichen wurde als schräge Wand behandelt.

**Auswertung:** Funktion der markierten Bruchgeometrie im Modell prüfen.

**Sollfälle:** SH22-T02 = `false`, SH22-T04 = `false`

## `flight_directions_separate`

Verschiedene Treppenläufe haben eigene Richtungsbezüge.

**Auswertung:** Richtung pro Lauf führen statt einen globalen Blattpfeil auf alle anzuwenden.

**Sollfälle:** SH22-T02 = `true`

## `opposite_flight_interpretation_supported`

Die gegenläufige Darstellung wird mit ihren Originalmerkmalen begründet.

**Auswertung:** Pfeile, Laufpositionen und Podestzuordnung beider Läufe vergleichen.

**Sollfälle:** SH22-T02 = `true`

## `relative_rise_separate_from_floor_id`

Relative Steigungssumme und absolute Zielgeschoss-ID bleiben getrennt.

**Auswertung:** Anzahl × Steigung auswerten und fehlende absolute Anschlüsse separat offen lassen.

**Sollfälle:** SH22-T03 = `true`, SH22-T04 = `true`

## `large_arc_function`

Funktion des großen Treppenbogens.

**Auswertung:** Ohne vollständigen Funktionsbeleg unknown; nicht allein Tür nennen.

**Sollfälle:** SH22-T05 = `"unknown"`

## `extra_door_invented`

Aus dem Großbogen wurde eine zusätzliche unbelegte Tür erzeugt.

**Auswertung:** Türinventur und Mechanik-/Öffnungsbeleg an T05 prüfen.

**Sollfälle:** SH22-T05 = `false`

## `unresolved_feature_retained`

Der ungeklärte Großbogen bleibt als ungeklärtes Merkmal nachvollziehbar.

**Auswertung:** Quellelement darf nicht still verschwinden oder als sicher klassifiziert werden.

**Sollfälle:** SH22-T05 = `true`

## `shaft_cabin_access_separate`

Liftschacht, Kabine und Zugang werden getrennt modelliert.

**Auswertung:** Bauteile, Flächen und Zugangsrelationen prüfen.

**Sollfälle:** SH22-L01 = `true`

## `entire_shaft_as_permanent_floor`

Der komplette Liftschacht wurde zu dauerhaftem Geschossboden.

**Auswertung:** Schachtaußenraum und Kabinenboden mit Freifläche vergleichen.

**Sollfälle:** SH22-L01 = `false`

## `cabin_access_conditional`

Liftkabinenzugang trägt die notwendigen Zustands-/Betriebsbedingungen.

**Auswertung:** Nicht als jederzeit offene unbedingte Gangverbindung ausgeben.

**Sollfälle:** SH22-L01 = `true`

## `fwa_expansion_unconditionally_proven`

Die ausgeschriebene Bedeutung von FWA wurde als endgültig belegt ausgegeben.

**Auswertung:** Zusätzliche Anlagenquelle prüfen; aus Paket allein bleibt die genaue Auflösung kontextgestützt.

**Sollfälle:** SH22-L01 = `false`

## `maintenance_walkway_and_ladder_distinguished`

Wartungssteg und Schachtleiter werden als unterschiedliche technische Elemente erkannt.

**Auswertung:** Textteile und passende Geometrien mit getrennten Funktionen verknüpfen.

**Sollfälle:** SH22-L02 = `true`

## `ordinary_corridor_edge`

Im technischen Wartungsbereich wurde eine gewöhnliche Gangverbindung angelegt.

**Auswertung:** Zugangsart und tatsächlich erzeugte Graphkante prüfen.

**Sollfälle:** SH22-L02 = `false`

## `technical_area_automatically_all_void`

Die ganze technische Fläche wurde ohne Differenzierung zum bodenlosen Loch erklärt.

**Auswertung:** Existenz eines Wartungsstegs und offene Restbereiche getrennt prüfen.

**Sollfälle:** SH22-L02 = `false`

## `fall_barrier_blocks_crossing`

Die Absturzsicherung verhindert das Queren ihres Randes.

**Auswertung:** Randgeometrie, Sperrfunktion und Graphkanten abgleichen.

**Sollfälle:** SH22-B01 = `true`, SH22-B02 = `true`

## `interior_general_floor_confirmed`

Die innere Fläche hinter der Sicherung wurde als allgemeiner Boden bestätigt.

**Auswertung:** False bedeutet hier nicht bestätigter Boden; keine Aussage über bewiesene völlige Bodenlosigkeit.

**Sollfälle:** SH22-B01 = `false`

## `void_depth`

Tiefe/unterer Abschluss des betreffenden Innenfelds.

**Auswertung:** Ohne Schnitt/Höhenbeleg unknown; raumhoch liefert keine Tiefe.

**Sollfälle:** SH22-B01 = `"unknown"`, SH22-B02 = `"unknown"`

## `raumhoch_creates_room`

Aus dem Sicherungstext wurde ein begehbarer Raum abgeleitet.

**Auswertung:** Textfunktion und erzeugte Raum-/Bodenobjekte prüfen.

**Sollfälle:** SH22-B01 = `false`

## `adjoining_terrace_floor_preserved`

Der belegte Terrassenboden außerhalb des gesicherten Bereichs bleibt erhalten.

**Auswertung:** Sperrung auf die richtige Rand-/Sonderfläche begrenzen.

**Sollfälle:** SH22-B02 = `true`

## `slope_lines_are_walls`

Gefällelinien wurden als feste Wände klassifiziert.

**Auswertung:** Ablauf-/Prozentbelege und Linienrollen prüfen.

**Sollfälle:** SH22-B03 = `false`

## `drain_text_used`

Der lokal zugeordnete Ablauftext fließt in die Interpretation ein.

**Auswertung:** Originaltext mit Ablaufzeichen und Entwässerungsgeometrie verknüpfen.

**Sollfälle:** SH22-B03 = `true`

## `terrace_split_into_triangular_rooms`

Gefällediagonalen erzeugen dreieckige neue Räume.

**Auswertung:** Raumgrenzen und Linienherkunft auf der Terrasse kontrollieren.

**Sollfälle:** SH22-B03 = `false`

## `water_layer_and_paving_slopes_separate`

Wasserführende Schicht und Plattenbelag haben getrennte Neigungsattribute.

**Auswertung:** Den zugehörigen Architektenhinweis nachweisbar auswerten.

**Sollfälle:** SH22-B04 = `true`

## `paving_slope_percent`

Zugeordneter Gefällewert des Plattenbelags in Prozent.

**Auswertung:** Zahlenwert 1 aus dem konkreten Hinweis, nicht aus der benachbarten Abdichtungsneigung lesen.

**Sollfälle:** SH22-B04 = `1`

## `water_layer_value_overwrites_paving`

Neigung der wasserführenden Schicht überschreibt den Belagwert.

**Auswertung:** Attributwerte und Schichtzuordnung prüfen.

**Sollfälle:** SH22-B04 = `false`

## `elevation_reference_preserved`

Höhenwerte behalten ihre eigene Bezugsebene.

**Auswertung:** FBOK/RDOK und Bauteilbezug mit Wert und Einheit speichern.

**Sollfälle:** SH22-B05 = `true`

## `overhead_line_automatically_wall`

Ein Hinweis auf einen oberen Bauteil wurde automatisch zur Bodenwand.

**Auswertung:** Höhenbeleg und Bodenwirkung getrennt prüfen.

**Sollfälle:** SH22-B05 = `false`

## `dimension_line_automatically_wall`

Eine Maßlinie wurde automatisch zur Wand.

**Auswertung:** Linienrolle, Maßtext und bauliche Sperrwirkung vergleichen.

**Sollfälle:** SH22-B05 = `false`

## `whole_profile_band_as_exit`

Das gesamte Fassadenprofilband wurde zum Ausgang.

**Auswertung:** Öffnungsart und untere Anschlusshöhe für jedes relevante Feld prüfen.

**Sollfälle:** SH22-F03 = `false`

## `lower_floor_connection_checked`

Der untere Anschluss wurde vor einer Gehpassage eigens geprüft.

**Auswertung:** Ein Sturzmaß oder Flügelbogen alleine reicht nicht.

**Sollfälle:** SH22-F03 = `true`

## `lintel_height_used_as_portal_proof`

Die Sturzunterkante allein wurde als Gehportalbeweis verwendet.

**Auswertung:** Beweiskette auf fehlenden unteren Bodenanschluss prüfen.

**Sollfälle:** SH22-F03 = `false`

## `room_id`

Am konkret lokalisierten Beispiel zugeordnete Original-Raum-ID.

**Auswertung:** Die ID aus dem zugeordneten Raumstempel lesen; keine Klassifikator-Konstante.

**Sollfälle:** SH22-R01 = `"3.16"`, SH22-R04 = `"3.06"`

## `room_and_free_floor_separate`

Raumfläche und darin verbleibender freier Boden sind getrennt.

**Auswertung:** Raumkontur und Hindernisabzug im Ergebnis unterscheiden.

**Sollfälle:** SH22-R01 = `true`

## `furniture_creates_extra_rooms`

Einrichtung erzeugt zusätzliche selbständige Räume.

**Auswertung:** Raumanzahl lokal und Grenzherkunft prüfen.

**Sollfälle:** SH22-R01 = `false`

## `mufu_is_usage_zone`

MUFU wird hier als offene Nutzungszone innerhalb der Erschließung geführt.

**Auswertung:** Nutzungs-ID darf ohne feste Umfassung keine neue Mauer verlangen.

**Sollfälle:** SH22-R02 = `true`

## `imaginary_enclosing_wall`

Zur MUFU-Beschriftung wurde eine nicht vorhandene Umfassung erfunden.

**Auswertung:** Produktive Grenzkanten mit Originalgeometrie abgleichen.

**Sollfälle:** SH22-R02 = `false`

## `open_floor_connection_preserved`

Die belegte offene Bodenverbindung der Nutzungszone bleibt erhalten.

**Auswertung:** Keine Sperre allein aus Raum-/Zonen-ID einfügen.

**Sollfälle:** SH22-R02 = `true`

## `leader_target_used`

Das Ziel der Textbezugslinie wurde für die Zuordnung verwendet.

**Auswertung:** Text → Bezugslinie → Zielraum konkret belegen.

**Sollfälle:** SH22-R03 = `true`

## `text_line_is_wall`

Eine Beschriftungsbezugslinie wird als Wand verwendet.

**Auswertung:** Linienrolle und Auswirkungen auf Raum/Boden kontrollieren.

**Sollfälle:** SH22-R03 = `false`

## `single_access_suffices`

Ein einziger belegter Zugang genügt für die Erreichbarkeit des Abstellraums.

**Auswertung:** Raum nicht wegen fehlendem zweiten Ausgang als Schacht verwerfen.

**Sollfälle:** SH22-R04 = `true`

## `free_floor_reaches_back`

Die freie Bodenfläche reicht bis zum belegten hinteren Raumende.

**Auswertung:** Innerhalb der Raumgrenzen verbleibenden Boden vollständig prüfen.

**Sollfälle:** SH22-R04 = `true`

## `full_free_floor_not_route_band`

Die Ausgabe erhält vollständige freie Bodenflächen statt nur einer Route.

**Auswertung:** Gesamtbreite, Nischen und Aufweitungen des Gangs gegen Original prüfen.

**Sollfälle:** SH22-G01 = `true`

## `furniture_gaps_preserved`

Freie Zwischenräume zwischen einzelnen Möbeln bleiben in G01 erhalten.

**Auswertung:** Kein Sammelrechteck als Stellfläche über die ganze Gruppe verwenden.

**Sollfälle:** SH22-G01 = `true`

## `edge_through_solid_wall`

Eine Graphkante quert den festen Wandkörper ohne Portalbeleg.

**Auswertung:** Graphgeometrie gegen Sperrflächen und verifizierte Portale prüfen.

**Sollfälle:** SH22-G01 = `false`

## `person_clearance_claim_without_metric_check`

Benutzbarkeit einer Engstelle wurde ohne Maß-/Profilprüfung behauptet.

**Auswertung:** Bestätigte Einheiten, Messwerte und gewähltes Bewegungsprofil verlangen.

**Sollfälle:** SH22-G01 = `false`
