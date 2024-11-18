import json
import os
class FitnessAssistant:
    def __init__(self):
        self.user_profile = {}
        self.profile_file = "user_profile.json"
    def save_profile(self):
        """Save user profile to a JSON file."""
        with open(self.profile_file, 'w') as f:
            json.dump(self.user_profile, f)
    def load_profile(self):
        """Load user profile from JSON file if it exists."""
        if os.path.exists(self.profile_file):
            with open(self.profile_file, 'r') as f:
                self.user_profile = json.load(f)
            return True
        return False
    def calculate_bmr(self, weight, height, age, gender):
        """Calculate Basal Metabolic Rate (BMR) based on the Mifflin-St Jeor equation."""
        if gender.lower() == 'male':
            bmr = 66 + (6.23 * weight) + (12.7 * height) - (6.8 * age)
        else:
            bmr = 655 + (4.35 * weight) + (4.7 * height) - (4.7 * age)
        return bmr
    def calculate_daily_calories(self, bmr, goal_weight, weight, activity_level, diet_type):
        """Calculate daily calorie needs based on multiple factors."""
        # Activity level multipliers
        activity_multipliers = {
            'sedentary': 1.2,
            'light': 1.375,
            'moderate': 1.55,
            'very active': 1.725,
            'extra active': 1.9
        }

        # Calculate calories with activity level
        daily_calories = bmr * activity_multipliers.get(activity_level.lower(), 1.2)

        # Adjust calories based on goal
        if goal_weight < weight:
            daily_calories -= 500  # Weight loss
        elif goal_weight > weight:
            daily_calories += 500  # Weight gain

        # Further adjustments based on diet type
        diet_adjustments = {
            'keto': -100,
            'paleo': 50,
            'vegetarian': -50,
            'vegan': -75,
            'standard': 0
        }
        daily_calories += diet_adjustments.get(diet_type.lower(), 0)

        return daily_calories

    def suggest_exercises(self, goal_weight, weight, fitness_goal, equipment_available):
        """Suggest exercises based on multiple factors."""
        exercise_categories = {
            'weight loss': [
                "High-Intensity Interval Training (HIIT)",
                "Cardio circuits",
                "Running or jogging",
                "Swimming"
            ],
            'muscle gain': [
                "Weightlifting",
                "Resistance training",
                "Compound movements",
                "Bodyweight exercises"
            ],
            'endurance': [
                "Long-distance running",
                "Cycling",
                "Swimming laps",
                "Cross-training"
            ]
        }

        # Filter exercises based on available equipment
        equipment_exercises = {
            'no equipment': [
                "Bodyweight squats",
                "Push-ups",
                "Lunges",
                "Planks",
                "Burpees"
            ],
            'basic home equipment': [
                "Dumbbell workouts",
                "Resistance band exercises",
                "Kettlebell swings"
            ],
            'full gym': [
                "Barbell squats",
                "Deadlifts",
                "Machine-based workouts",
                "Cable machine exercises"
            ]
        }

        # Combine exercises from goal and equipment
        suggested_exercises = (
                exercise_categories.get(fitness_goal.lower(), []) +
                equipment_exercises.get(equipment_available.lower(), [])
        )

        return list(set(suggested_exercises))[:6]

    def create_personalized_diet_plan(self, diet_type, allergies, preferences):
        """Create a more personalized diet plan."""
        base_diet_plans = {
            'keto': {
                "Monday": "Avocado and eggs, grilled chicken salad, salmon with asparagus",
                "Tuesday": "Chia seed pudding, tuna salad, beef stir-fry",
                "Wednesday": "Egg muffins, cauliflower rice with shrimp, pork chops with zucchini",
                "Thursday": "Keto smoothie, chicken Caesar salad, lamb chops with roasted vegetables",
                "Friday": "Frittata, tuna stuffed avocado, steak with spinach",
                "Saturday": "Bacon and eggs, cobb salad, salmon with asparagus",
                "Sunday": "Keto pancakes, seafood salad, roast beef with cauliflower mash"
            },
            'vegetarian': {
                "Monday": "Tofu scramble, quinoa salad, lentil curry",
                "Tuesday": "Greek yogurt parfait, veggie wrap, bean chili",
                "Wednesday": "Chia seed breakfast bowl, Mediterranean salad, vegetable stir-fry",
                "Thursday": "Spinach and mushroom omelette, chickpea buddha bowl, stuffed bell peppers",
                "Friday": "Smoothie bowl, falafel wrap, vegetable lasagna",
                "Saturday": "Avocado toast, tempeh salad, eggplant parmesan",
                "Sunday": "Pancakes with fruit, quinoa salad, vegetable curry"
            },
            'standard': {
                "Monday": "Oatmeal with berries, turkey sandwich, chicken with rice",
                "Tuesday": "Smoothie, salad with grilled protein, fish with vegetables",
                "Wednesday": "Eggs and toast, chicken Caesar salad, beef stir-fry",
                "Thursday": "Greek yogurt with granola, tuna sandwich, pork tenderloin with sweet potato",
                "Friday": "Protein shake, wrap with lean meat, salmon with quinoa",
                "Saturday": "Pancakes with fruit, chef salad, grilled shrimp",
                "Sunday": "Eggs Benedict, grilled chicken salad, roast turkey with vegetables"
            }
        }

        # Remove allergens and apply preferences
        diet_plan = base_diet_plans.get(diet_type.lower(), base_diet_plans['standard'])

        # Simple allergen and preference filtering
        if 'dairy' in allergies:
            diet_plan = {day: meals.replace('yogurt', 'coconut yogurt').replace('cheese', 'nutritional yeast')
                         for day, meals in diet_plan.items()}

        if 'gluten' in allergies:
            diet_plan = {day: meals.replace('sandwich', 'salad').replace('wrap', 'lettuce wrap').replace('toast',
                                                                                                         'gluten-free toast')
                         for day, meals in diet_plan.items()}

        return diet_plan
    def collect_user_details(self):
        """Collect comprehensive user details with more options."""
        print("Welcome to your Advanced Personalized Nutrition and Fitness AI Assistant!")

        # Check for existing profile
        if self.load_profile():
            print("Existing profile found. Let's update your information.")

        # Comprehensive user input
        self.user_profile['weight'] = float(input("Enter your current weight (in lbs): "))
        feet = int(input("Enter your height (feet): "))
        inches = int(input("Enter your height (inches): "))
        self.user_profile['height'] = (feet * 12) + inches
        self.user_profile['age'] = int(input("Enter your age: "))
        self.user_profile['gender'] = input("Enter your gender (male/female): ")
        self.user_profile['goal_weight'] = float(input("Enter your goal weight (in lbs): "))

        # Additional detailed inputs
        self.user_profile['activity_level'] = input(
            "Enter your activity level (sedentary/light/moderate/very active/extra active): ")
        self.user_profile['fitness_goal'] = input(
            "Enter your primary fitness goal (weight loss/muscle gain/endurance): ")
        self.user_profile['diet_type'] = input("Enter your preferred diet type (standard/keto/vegetarian/paleo): ")
        self.user_profile['equipment_available'] = input(
            "Equipment available (no equipment/basic home equipment/full gym): ")
        self.user_profile['allergies'] = input("List any food allergies (comma-separated, or 'none'): ").split(',')
        self.user_profile['dietary_preferences'] = input(
            "Any dietary preferences (comma-separated, or 'none'): ").split(',')

        # Save profile
        self.save_profile()
        return self.user_profile
    def generate_recommendations(self, profile):
        """Generate comprehensive recommendations based on user profile."""
        # Calculate daily calories
        daily_calories = self.calculate_daily_calories(
            self.calculate_bmr(
                profile['weight'],
                profile['height'],
                profile['age'],
                profile['gender']
            ),
            profile['goal_weight'],
            profile['weight'],
            profile['activity_level'],
            profile['diet_type']
        )

        # Goal-specific calorie guidance
        if profile['goal_weight'] < profile['weight']:
            calorie_guidance = f"To lose weight: Aim for {daily_calories:.0f} calories per day"
        elif profile['goal_weight'] > profile['weight']:
            calorie_guidance = f"To gain weight: Aim for {daily_calories:.0f} calories per day"
        else:
            calorie_guidance = f"To maintain weight: Aim for {daily_calories:.0f} calories per day"

        # Get exercise suggestions
        exercises = self.suggest_exercises(
            profile['goal_weight'],
            profile['weight'],
            profile['fitness_goal'],
            profile['equipment_available']
        )

        # Create diet plan
        diet_plan = self.create_personalized_diet_plan(
            profile['diet_type'],
            profile['allergies'],
            profile['dietary_preferences']
        )

        # Display results
        print("\n--- Daily Calorie Recommendation ---")
        print(calorie_guidance)
        print("\nNote: These recommendations are estimates. Consult a nutritionist for personalized advice.")

        print("\n--- Exercise Recommendations ---")
        for exercise in exercises:
            print(f"- {exercise}")

        print("\n--- Personalized Diet Plan ---")
        for day, meals in diet_plan.items():
            print(f"{day}: {meals}")

    def run(self):
        """Main method to run the fitness assistant."""
        profile = self.collect_user_details()
        self.generate_recommendations(profile)


def main():
    assistant = FitnessAssistant()
    assistant.run()

if __name__ == "__main__":
    main()
