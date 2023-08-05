import sys
import json
from generator import TemplateGenerator

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python main.py <num_linked_individuals> <num_linked_organizations> <iso_country_code>")
        sys.exit(1)

    num_linked_individuals = int(sys.argv[1])
    num_linked_organizations = int(sys.argv[2])
    iso_country_code = sys.argv[3]

    template_generator = TemplateGenerator(iso_country_code)
    output_data = template_generator.generate_template(num_linked_individuals, num_linked_organizations)

    output_file = f"{output_data['details']['organizationName']}_{iso_country_code}.json"
    with open(output_file, "w", encoding="utf-8") as f:
            json.dump(output_data, f, ensure_ascii=False, indent=4)

    print(f"Generated output file: {output_file}")
