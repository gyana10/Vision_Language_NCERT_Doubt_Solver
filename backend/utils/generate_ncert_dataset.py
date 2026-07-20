import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(BASE_DIR, "data")

NCERT_CURRICULUM = {
    "class5": {
        "science": [
            ("Chapter 1: Super Senses", "Animals have amazing senses of sight, smell, hearing, and touch. Dogs can mark their area by smell. Ants leave a trail of scent (pheromones) so other ants can follow. Mosquitoes can find humans by the heat and smell of their feet."),
            ("Chapter 2: From Tasting to Digesting", "Digestion starts in the mouth when saliva breaks down food. Glucose gives instant energy. The stomach churns food with digestive juices and acid to break down nutrients."),
            ("Chapter 3: Seeds and Seeds", "Seeds need water, air, and proper temperature to germinate. Seeds disperse by wind, water, animals, and bursting pods. Pitcher plants (Nepenthes) trap and digest insects for nitrogen."),
            ("Chapter 4: Experiments with Water", "Objects float if they displace water equal to their weight. Dissolved substances like salt make water denser, helping objects float easier like in the Dead Sea.")
        ],
        "maths": [
            ("Chapter 1: The Fish Tale", "Speed = Distance / Time. Area of rectangle = length x width. Perimeter of rectangle = 2 x (length + width). One lakh = 100,000. One crore = 10,000,000."),
            ("Chapter 2: Shapes and Angles", "Right angle measures exactly 90 degrees. Acute angle is less than 90 degrees. Obtuse angle is greater than 90 degrees and less than 180 degrees. Straight angle is 180 degrees."),
            ("Chapter 3: Parts and Wholes", "Fractions represent equal parts of a whole. Half is 1/2, quarter is 1/4, three-quarters is 3/4. Equivalent fractions have equal value like 1/2 = 2/4 = 3/6.")
        ],
        "sst": [
            ("Chapter 1: Our Country India", "India is located in the Northern Hemisphere. The Tropic of Cancer passes through India. India has 28 states and 8 Union Territories. The Himalayas form the northern boundary."),
            ("Chapter 2: Maps and Globes", "A globe is a three-dimensional model of Earth. A map is a representation of Earth's surface on a flat paper. Cardinal directions are North, South, East, and West.")
        ]
    },
    "class6": {
        "science": [
            ("Chapter 1: Components of Food", "Carbohydrates and fats provide energy to the body. Proteins are needed for growth and repair of our body. Vitamins and minerals protect our body against diseases. Deficiency of Vitamin C causes scurvy, Vitamin D causes rickets, Vitamin A causes night blindness, Iron causes anemia, Iodine causes goitre."),
            ("Chapter 2: Sorting Materials into Groups", "Materials can be grouped based on appearance, hardness, solubility, transparency, and density. Soluble substances dissolve in water. Transparent materials allow light to pass through completely, translucent materials allow partial light, and opaque materials block light entirely."),
            ("Chapter 3: Getting to Know Plants", "Herbs have green tender stems. Shrubs have woody stems branching near the base. Trees have hard thick brown stems. Leaves perform photosynthesis using chlorophyll, sunlight, carbon dioxide, and water. Taproot system has a main root; fibrous root system has a cluster of similar roots."),
            ("Chapter 4: Electricity and Circuits", "An electric cell converts chemical energy into electrical energy. Electric circuit provides a closed continuous path for electric current to flow from positive to negative terminal. Conductors allow electricity to pass through; insulators do not.")
        ],
        "sst": [
            ("Chapter 1: Globe Latitudes and Longitudes", "Latitude lines run east-west parallel to the Equator (0 degrees). Longitude lines run north-south through the poles. The Prime Meridian is 0 degrees longitude passing through Greenwich. Standard Meridian of India is 82.5 degrees East (IST)."),
            ("Chapter 2: Major Domains of the Earth", "The four major domains of Earth are Lithosphere (land), Atmosphere (air), Hydrosphere (water), and Biosphere (living narrow zone where land, air, and water interact).")
        ]
    },
    "class7": {
        "science": [
            ("Chapter 1: Nutrition in Plants", "Autotrophic nutrition is practiced by green plants through photosynthesis: Carbon dioxide + Water + Sunlight + Chlorophyll -> Glucose + Oxygen. Heterotrophic plants include parasitic plants like Cuscuta (Amarbel) and insectivorous plants like Pitcher plant."),
            ("Chapter 2: Heat and Temperature", "Temperature is a measure of the degree of hotness of an object. Clinical thermometer measures temperature from 35C to 42C. Conduction is heat transfer in solids. Convection is heat transfer in liquids and gases. Radiation is heat transfer without any medium."),
            ("Chapter 3: Acids, Bases and Salts", "Acids taste sour and turn blue litmus paper red. Bases taste bitter, feel soapy, and turn red litmus blue. Neutralization reaction: Acid + Base -> Salt + Water + Heat. Litmus is a natural indicator extracted from lichens.")
        ],
        "sst": [
            ("Chapter 1: Environment and Ecosystem", "Environment consists of natural (biotic and abiotic) and human-made components. Atmosphere protects us from harmful rays of the sun. Hydrosphere includes all water bodies on Earth.")
        ]
    },
    "class8": {
        "science": [
            ("Chapter 1: Crop Production and Management", "Preparation of soil includes plowing and leveling. Sowing requires good quality seeds. Manure is organic; fertilizers are chemical compounds rich in nitrogen, phosphorus, and potassium (NPK). Drip irrigation saves water by supplying water drop by drop near the roots."),
            ("Chapter 2: Microorganisms: Friend and Foe", "Bacteria, fungi, protozoa, and algae are major microorganisms. Viruses reproduce only inside host cells. Rhizobium bacteria fix atmospheric nitrogen in leguminous plants. Pasteurization heats milk to 70C for 15-30 seconds to kill harmful microbes."),
            ("Chapter 3: Force and Pressure", "Force is a push or pull acting on an object. Pressure = Force / Area. Unit of force is Newton (N), unit of pressure is Pascal (Pa). Friction opposes motion between two surfaces in contact.")
        ],
        "sst": [
            ("Chapter 1: The Indian Constitution", "The Indian Constitution guarantees Fundamental Rights: Right to Equality, Right to Freedom, Right against Exploitation, Right to Freedom of Religion, Cultural and Educational Rights, and Right to Constitutional Remedies. India is a Secular Democratic Republic.")
        ]
    },
    "class9": {
        "science": [
            ("Chapter 1: Matter in Our Surroundings", "Matter exists in three states: Solid, Liquid, and Gas. Evaporation causes cooling. Latent heat of vaporization is heat absorbed when liquid changes to gas at constant temperature."),
            ("Chapter 2: The Fundamental Unit of Life (Cell)", "Cell is the structural and functional unit of life. Mitochondria is the powerhouse of the cell producing ATP. Lysosomes are suicide bags containing digestive enzymes. Plant cells have cell wall, chloroplasts, and large central vacuole."),
            ("Chapter 3: Motion and Gravitation", "First Law of Motion (Inertia): An object remains at rest or uniform motion unless acted upon by an external force. Second Law: F = m x a. Third Law: To every action there is an equal and opposite reaction. Universal Law of Gravitation: F = G * (m1 * m2) / r^2.")
        ],
        "sst": [
            ("Chapter 1: Physical Features of India", "The six physical divisions of India are: The Himalayan Mountains, The Northern Plains, The Peninsular Plateau, The Indian Desert, The Coastal Plains, and The Islands (Lakshadweep and Andaman & Nicobar).")
        ]
    },
    "class10": {
        "science": [
            ("Chapter 1: Chemical Reactions and Equations", "Combination reaction combines two reactants into one product. Decomposition reaction breaks one reactant into simpler products. Oxidation is gain of oxygen or loss of hydrogen. Reduction is loss of oxygen or gain of hydrogen. Exothermic reactions release heat; endothermic reactions absorb heat."),
            ("Chapter 2: Life Processes", "Life processes include nutrition, respiration, transportation, and excretion. Photosynthesis takes place in chloroplasts. Aerobic respiration produces 38 ATP molecules per glucose in mitochondria. Human heart has 4 chambers: two atria and two ventricles. Nephrons are the filtration units of kidneys."),
            ("Chapter 3: Light - Reflection and Refraction", "Law of Reflection: Angle of incidence = Angle of reflection. Mirror formula: 1/f = 1/v + 1/u. Lens formula: 1/f = 1/v - 1/u. Power of lens P = 1 / f(in meters), measured in Dioptres (D). Convex lens is converging; concave lens is diverging.")
        ],
        "sst": [
            ("Chapter 1: Federalism and Power Sharing", "Federalism is a system of government in which power is divided between a central authority and various constituent units. Union List, State List, and Concurrent List divide legislative powers in India.")
        ]
    }
}

def create_pdf(file_path, subject, chapters):
    doc = SimpleDocTemplate(file_path, pagesize=letter)
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontSize=20,
        leading=24,
        textColor='#1a365d',
        spaceAfter=15
    )
    heading_style = ParagraphStyle(
        'ChapterHeading',
        parent=styles['Heading2'],
        fontSize=14,
        leading=18,
        textColor='#2b6cb0',
        spaceBefore=10,
        spaceAfter=6
    )
    body_style = ParagraphStyle(
        'BodyText',
        parent=styles['Normal'],
        fontSize=11,
        leading=16,
        spaceAfter=12
    )

    story = []
    story.append(Paragraph(f"NCERT Textbook - {subject.upper()}", title_style))
    story.append(Spacer(1, 10))

    for title, content in chapters:
        story.append(Paragraph(title, heading_style))
        story.append(Paragraph(content, body_style))
        story.append(Spacer(1, 8))

    doc.build(story)

def main():
    print("Generating structured NCERT PDFs for dataset completeness...")
    for class_name, subjects in NCERT_CURRICULUM.items():
        class_dir = os.path.join(DATA_DIR, class_name)
        os.makedirs(class_dir, exist_ok=True)
        for subject, chapters in subjects.items():
            pdf_path = os.path.join(class_dir, f"{subject}.pdf")
            if not os.path.exists(pdf_path):
                print(f"Creating missing PDF: {pdf_path}")
                create_pdf(pdf_path, subject, chapters)
            else:
                print(f"PDF already exists: {pdf_path}")

if __name__ == "__main__":
    main()
