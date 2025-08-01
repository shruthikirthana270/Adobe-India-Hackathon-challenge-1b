#!/usr/bin/env python3
"""
Create proper PDF files with actual content for Challenge 1b testing
"""

import sys
from pathlib import Path

def install_reportlab():
    """Install reportlab if not available."""
    try:
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import letter
        return True
    except ImportError:
        print("📦 Installing reportlab...")
        import subprocess
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "reportlab"])
            from reportlab.pdfgen import canvas
            from reportlab.lib.pagesizes import letter
            return True
        except:
            print("❌ Could not install reportlab")
            return False

def create_detailed_pdf(filepath, title, content_sections):
    """Create a detailed PDF with multiple sections."""
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import getSampleStyleSheet
    
    c = canvas.Canvas(str(filepath), pagesize=letter)
    width, height = letter
    
    # Title page
    c.setFont('Helvetica-Bold', 20)
    c.drawString(50, height - 80, title)
    
    c.setFont('Helvetica', 12)
    y_position = height - 120
    
    for section_title, section_content in content_sections.items():
        # Section header
        if y_position < 100:
            c.showPage()
            y_position = height - 50
        
        c.setFont('Helvetica-Bold', 14)
        c.drawString(50, y_position, section_title)
        y_position -= 25
        
        # Section content
        c.setFont('Helvetica', 11)
        
        # Split content into lines and handle wrapping
        lines = section_content.split('\n')
        for line in lines:
            if not line.strip():
                y_position -= 10
                continue
                
            # Simple word wrapping
            words = line.split()
            current_line = ""
            
            for word in words:
                test_line = current_line + word + " "
                if len(test_line) > 85:  # Approximate character limit
                    if current_line:
                        if y_position < 50:
                            c.showPage()
                            y_position = height - 50
                        c.drawString(50, y_position, current_line.strip())
                        y_position -= 15
                    current_line = word + " "
                else:
                    current_line = test_line
            
            # Draw remaining text
            if current_line.strip():
                if y_position < 50:
                    c.showPage()
                    y_position = height - 50
                c.drawString(50, y_position, current_line.strip())
                y_position -= 15
        
        y_position -= 20  # Extra space between sections
    
    c.save()

def create_travel_guide():
    """Create a comprehensive travel guide PDF."""
    content = {
        "Introduction to South of France": """
        The South of France, known as the French Riviera or Côte d'Azur, is one of Europe's most glamorous destinations. This region offers stunning Mediterranean coastlines, charming medieval villages, world-class cuisine, and vibrant cultural experiences perfect for group travel.
        
        For college students planning a 4-day trip, this guide provides essential information on budget-friendly accommodations, group activities, transportation options, and must-see attractions that will create unforgettable memories.
        """,
        
        "Budget Planning for Groups": """
        Planning a trip for 10 college friends requires careful budget management. Here are key considerations:
        
        Accommodation: Look for hostels with group rooms, vacation rentals, or budget hotels that offer group discounts. Expect to spend 25-40 euros per person per night.
        
        Transportation: Group train tickets and bus passes offer significant savings. Consider renting a van for day trips to nearby attractions.
        
        Food: Take advantage of local markets, picnic opportunities, and group meal deals at restaurants. Budget 30-50 euros per person per day for meals.
        
        Activities: Many museums and attractions offer student discounts. Beach activities and hiking are free and perfect for groups.
        """,
        
        "4-Day Itinerary Suggestions": """
        Day 1: Arrival in Nice
        - Check into accommodation
        - Explore Old Town (Vieux Nice)
        - Visit the famous Promenade des Anglais
        - Group dinner at a local bistro
        
        Day 2: Cannes and Antibes
        - Morning train to Cannes
        - Walk the famous Croisette boulevard
        - Afternoon in Antibes old town
        - Beach time and water activities
        
        Day 3: Monaco and Monte Carlo
        - Day trip to Monaco
        - Visit the Prince's Palace
        - Explore Monte Carlo (even if just window shopping!)
        - Return to Nice for evening activities
        
        Day 4: Local Exploration
        - Visit local markets
        - Hiking in nearby hills
        - Final group meal
        - Departure preparations
        """,
        
        "Group Activities and Entertainment": """
        Beach Activities: The Mediterranean offers perfect conditions for swimming, beach volleyball, and water sports. Many beaches have equipment rental for groups.
        
        Cultural Experiences: Visit local museums, art galleries, and historic sites. Many offer group rates and guided tours in English.
        
        Nightlife: The French Riviera has vibrant nightlife suitable for college students. Beach clubs, bars, and local festivals provide entertainment options.
        
        Outdoor Adventures: Hiking trails, bike rentals, and boat trips offer active group experiences with stunning scenery.
        
        Food and Wine: Cooking classes, wine tastings, and food tours provide cultural immersion and group bonding opportunities.
        """,
        
        "Transportation Guide": """
        Getting There: Fly into Nice Côte d'Azur Airport, which has good connections to major European cities. Group bookings often receive discounts.
        
        Local Transportation: The regional train system connects all major coastal cities. Purchase group passes for savings.
        
        Bus Services: Local buses are economical and connect smaller towns and beaches not served by trains.
        
        Rental Options: For maximum flexibility, consider renting a van or multiple cars. Ensure drivers have international licenses.
        
        Walking and Cycling: Many attractions are walkable, and bike rentals are available in most cities.
        """
    }
    
    filepath = Path("Collection 1/PDFs/travel_guide.pdf")
    create_detailed_pdf(filepath, "South of France Travel Guide for College Groups", content)
    print(f"✅ Created: {filepath}")

def create_forms_guide():
    """Create an Adobe Forms guide PDF."""
    content = {
        "Introduction to Adobe Acrobat Forms": """
        Adobe Acrobat provides powerful tools for creating fillable PDF forms essential for HR processes. This guide covers the fundamentals of form creation, from basic field types to advanced automation features.
        
        For HR professionals managing onboarding and compliance, digital forms streamline processes, reduce errors, and improve data collection efficiency. Modern organizations require digital-first approaches to documentation.
        """,
        
        "Form Field Types and Properties": """
        Text Fields: Used for collecting written information like names, addresses, and comments. Configure character limits, validation rules, and formatting options.
        
        Checkboxes: Perfect for yes/no questions, multiple choice selections, and consent acknowledgments. Essential for compliance documentation.
        
        Radio Buttons: Use for single-selection options like employment status, department selection, or preference choices.
        
        Dropdown Lists: Efficient for standardized selections like job titles, locations, or predefined categories.
        
        Digital Signatures: Critical for legal compliance and document authentication in HR processes.
        """,
        
        "HR Onboarding Forms": """
        Employee Information Forms: Collect personal details, emergency contacts, and basic employment information. Include validation to ensure data accuracy.
        
        Tax and Benefits Forms: Create fillable versions of W-4, I-9, and benefits enrollment forms. Ensure compliance with current regulations.
        
        Policy Acknowledgment Forms: Digital forms for employee handbook, safety policies, and code of conduct acknowledgments.
        
        Direct Deposit and Payroll: Secure forms for banking information and payroll preferences with appropriate security measures.
        
        Training and Certification: Track completion of required training programs and maintain certification records.
        """,
        
        "Compliance and Legal Requirements": """
        Data Privacy: Ensure forms comply with GDPR, CCPA, and other privacy regulations. Include appropriate consent mechanisms.
        
        Accessibility: Design forms that meet ADA compliance requirements. Use proper tab order, labels, and screen reader compatibility.
        
        Audit Trails: Implement tracking for form completion, modifications, and approvals. Maintain records for compliance purposes.
        
        Security Measures: Use password protection, encryption, and access controls for sensitive HR information.
        
        Retention Policies: Establish clear guidelines for how long form data is stored and when it should be deleted.
        """,
        
        "Workflow Automation": """
        Form Routing: Set up automatic routing of completed forms to appropriate HR personnel or departments.
        
        Approval Processes: Create multi-step approval workflows for forms requiring management sign-off.
        
        Integration with HR Systems: Connect forms to existing HRIS, payroll, and benefits administration systems.
        
        Notification Systems: Automated emails and reminders for incomplete forms or required actions.
        
        Reporting and Analytics: Generate reports on form completion rates, processing times, and common issues.
        """
    }
    
    filepath = Path("Collection 2/PDFs/forms_guide.pdf")
    create_detailed_pdf(filepath, "Adobe Acrobat Forms for HR Professionals", content)
    print(f"✅ Created: {filepath}")

def create_recipe_guide():
    """Create a vegetarian catering guide PDF."""
    content = {
        "Introduction to Vegetarian Corporate Catering": """
        Vegetarian catering for corporate events requires careful planning, creative menu design, and attention to dietary restrictions. This guide provides professional recipes and techniques for successful buffet-style service.
        
        Modern corporate events increasingly demand vegetarian options that are both delicious and visually appealing. Professional caterers must balance nutrition, presentation, cost-effectiveness, and scalability.
        """,
        
        "Menu Planning for Corporate Events": """
        Appetizers and Starters: Offer variety with hummus platters, vegetable crudités, stuffed mushrooms, and artisanal cheese selections. Consider dietary restrictions and allergies.
        
        Main Course Options: Feature substantial dishes like vegetarian lasagna, quinoa-stuffed bell peppers, mushroom wellington, and curry dishes that satisfy without meat.
        
        Side Dishes: Complement mains with roasted seasonal vegetables, grain salads, and creative potato preparations.
        
        Dessert Selection: Provide options including fresh fruit displays, vegetarian-friendly pastries, and dairy-free alternatives.
        
        Beverage Pairings: Consider wine selections, specialty teas, and fresh juice options that complement vegetarian flavors.
        """,
        
        "Buffet Service Planning": """
        Layout Design: Plan traffic flow to prevent bottlenecks. Position popular items strategically and ensure easy access for all guests.
        
        Temperature Control: Maintain proper temperatures for hot and cold items. Use chafing dishes, ice baths, and warming trays effectively.
        
        Presentation Techniques: Create visually appealing displays with height variation, color contrast, and attractive serving pieces.
        
        Portion Control: Calculate appropriate quantities based on guest count, event duration, and meal timing.
        
        Service Staff: Train staff on vegetarian ingredients, dietary restrictions, and proper serving techniques.
        """,
        
        "Scaling Recipes for Large Groups": """
        Recipe Conversion: Understand how to scale recipes from 4-6 servings to 50-100 portions while maintaining flavor balance.
        
        Ingredient Sourcing: Establish relationships with suppliers for bulk vegetarian ingredients. Consider seasonal availability and cost fluctuations.
        
        Preparation Timing: Create detailed prep schedules that account for cooking times, cooling periods, and assembly requirements.
        
        Equipment Needs: Ensure adequate commercial kitchen equipment for large-batch cooking and holding.
        
        Quality Control: Maintain consistent flavor and presentation across large quantities through systematic testing and adjustment.
        """,
        
        "Dietary Restrictions and Allergies": """
        Vegan Options: Provide clearly marked vegan dishes using plant-based ingredients exclusively. Avoid cross-contamination.
        
        Gluten-Free Choices: Offer gluten-free alternatives and ensure proper preparation to prevent cross-contamination.
        
        Nut Allergies: Clearly label dishes containing nuts and provide nut-free alternatives for sensitive guests.
        
        Religious Considerations: Understand kosher, halal, and other religious dietary requirements that may apply.
        
        Labeling and Communication: Provide clear, accurate labeling of all dishes with ingredient information and allergen warnings.
        """,
        
        "Cost Management and Profitability": """
        Ingredient Costing: Calculate accurate food costs including waste, preparation time, and overhead expenses.
        
        Seasonal Menu Planning: Design menus around seasonal ingredients to control costs and ensure freshness.
        
        Waste Reduction: Implement strategies to minimize food waste through accurate portioning and creative use of ingredients.
        
        Pricing Strategies: Develop competitive pricing that covers costs while providing reasonable profit margins.
        
        Client Communication: Clearly communicate value proposition and unique aspects of vegetarian catering services.
        """
    }
    
    filepath = Path("Collection 3/PDFs/recipe_guide.pdf")
    create_detailed_pdf(filepath, "Professional Vegetarian Catering Guide", content)
    print(f"✅ Created: {filepath}")

def main():
    """Create all proper PDF files."""
    print("📝 Creating proper PDF files with detailed content...")
    
    if not install_reportlab():
        print("❌ Cannot create PDFs without reportlab")
        return False
    
    # Ensure directories exist
    for i in range(1, 4):
        Path(f"Collection {i}/PDFs").mkdir(parents=True, exist_ok=True)
    
    # Create detailed PDFs
    create_travel_guide()
    create_forms_guide()
    create_recipe_guide()
    
    print("\n✅ All detailed PDF files created successfully!")
    print("\n🔄 Now run: python process_collections.py")
    print("Then run: python validate_outputs.py")
    
    return True

if __name__ == "__main__":
    main()
