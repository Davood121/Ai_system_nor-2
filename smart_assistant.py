import time
from datetime import datetime, timedelta
import json

class SmartAssistant:
    def __init__(self):
        self.reminders = []
        self.habits = {}
        self.goals = {}
        self.daily_insights = []
        
    def set_reminder(self, message, time_str, repeat=False):
        """Set intelligent reminders"""
        reminder = {
            'id': len(self.reminders) + 1,
            'message': message,
            'time': time_str,
            'repeat': repeat,
            'created': datetime.now().isoformat(),
            'active': True
        }
        
        self.reminders.append(reminder)
        
        # Store reminder for manual checking
        # Note: Advanced scheduling would require additional setup
        
        return f"Reminder set for {time_str}: {message}"
    
    def trigger_reminder(self, reminder_id):
        """Trigger a reminder"""
        reminder = next((r for r in self.reminders if r['id'] == reminder_id), None)
        if reminder and reminder['active']:
            print(f"🔔 Reminder: {reminder['message']}")
            return reminder['message']
    
    def track_habit(self, habit_name, completed=True):
        """Track daily habits"""
        today = datetime.now().date().isoformat()
        
        if habit_name not in self.habits:
            self.habits[habit_name] = {
                'created': datetime.now().isoformat(),
                'streak': 0,
                'total_days': 0,
                'history': {}
            }
        
        self.habits[habit_name]['history'][today] = completed
        
        if completed:
            self.habits[habit_name]['total_days'] += 1
            # Calculate streak
            self.calculate_streak(habit_name)
        
        return f"Habit '{habit_name}' marked as {'completed' if completed else 'missed'}"
    
    def calculate_streak(self, habit_name):
        """Calculate current streak for a habit"""
        if habit_name not in self.habits:
            return 0
        
        history = self.habits[habit_name]['history']
        streak = 0
        
        # Check backwards from today
        current_date = datetime.now().date()
        while current_date.isoformat() in history and history[current_date.isoformat()]:
            streak += 1
            current_date -= timedelta(days=1)
        
        self.habits[habit_name]['streak'] = streak
        return streak
    
    def set_goal(self, goal_name, target_value, target_date, unit=''):
        """Set and track goals"""
        goal = {
            'name': goal_name,
            'target_value': target_value,
            'target_date': target_date,
            'unit': unit,
            'current_progress': 0,
            'created': datetime.now().isoformat(),
            'milestones': []
        }
        
        self.goals[goal_name] = goal
        return f"Goal set: {goal_name} - {target_value} {unit} by {target_date}"
    
    def update_goal_progress(self, goal_name, progress_value):
        """Update progress on a goal"""
        if goal_name in self.goals:
            self.goals[goal_name]['current_progress'] = progress_value
            
            # Check for milestones
            target = self.goals[goal_name]['target_value']
            percentage = (progress_value / target) * 100
            
            milestone_message = ""
            if percentage >= 25 and '25%' not in [m['type'] for m in self.goals[goal_name]['milestones']]:
                milestone = {'type': '25%', 'date': datetime.now().isoformat()}
                self.goals[goal_name]['milestones'].append(milestone)
                milestone_message = "🎉 25% milestone reached!"
            elif percentage >= 50 and '50%' not in [m['type'] for m in self.goals[goal_name]['milestones']]:
                milestone = {'type': '50%', 'date': datetime.now().isoformat()}
                self.goals[goal_name]['milestones'].append(milestone)
                milestone_message = "🎉 Halfway there! 50% milestone reached!"
            elif percentage >= 75 and '75%' not in [m['type'] for m in self.goals[goal_name]['milestones']]:
                milestone = {'type': '75%', 'date': datetime.now().isoformat()}
                self.goals[goal_name]['milestones'].append(milestone)
                milestone_message = "🎉 75% milestone reached! Almost there!"
            elif percentage >= 100 and '100%' not in [m['type'] for m in self.goals[goal_name]['milestones']]:
                milestone = {'type': '100%', 'date': datetime.now().isoformat()}
                self.goals[goal_name]['milestones'].append(milestone)
                milestone_message = "🏆 Goal completed! Congratulations!"
            
            return f"Progress updated: {progress_value}/{target} {self.goals[goal_name]['unit']} ({percentage:.1f}%) {milestone_message}"
        
        return "Goal not found"
    
    def get_daily_summary(self):
        """Generate daily summary and insights"""
        today = datetime.now().date().isoformat()
        summary = []
        
        # Habit summary
        completed_habits = 0
        total_habits = len(self.habits)
        
        for habit_name, habit_data in self.habits.items():
            if today in habit_data['history'] and habit_data['history'][today]:
                completed_habits += 1
        
        if total_habits > 0:
            summary.append(f"📊 Habits: {completed_habits}/{total_habits} completed today")
        
        # Goal progress
        active_goals = len(self.goals)
        if active_goals > 0:
            summary.append(f"🎯 You have {active_goals} active goals")
        
        # Streaks
        best_streak = 0
        best_habit = ""
        for habit_name, habit_data in self.habits.items():
            if habit_data['streak'] > best_streak:
                best_streak = habit_data['streak']
                best_habit = habit_name
        
        if best_streak > 0:
            summary.append(f"🔥 Best streak: {best_habit} ({best_streak} days)")
        
        return "\\n".join(summary) if summary else "No activity tracked yet"
    
    def get_motivational_message(self):
        """Generate motivational messages based on progress"""
        messages = [
            "Every small step counts towards your bigger goals! 💪",
            "Consistency is key - keep building those habits! 🌟",
            "You're making progress every day! 🚀",
            "Remember: progress, not perfection! ✨",
            "Your future self will thank you for today's efforts! 🙏"
        ]
        
        # Personalize based on current streaks
        best_streak = 0
        for habit_data in self.habits.values():
            if habit_data['streak'] > best_streak:
                best_streak = habit_data['streak']
        
        if best_streak >= 7:
            messages.insert(0, f"Amazing! You've got a {best_streak}-day streak going! 🔥")
        elif best_streak >= 3:
            messages.insert(0, f"Great job on your {best_streak}-day streak! Keep it up! 💫")
        
        import random
        return random.choice(messages)
    
    def smart_suggestions(self):
        """Provide intelligent suggestions based on user patterns"""
        suggestions = []
        
        # Analyze habit patterns
        today_weekday = datetime.now().weekday()  # 0 = Monday
        
        # Check if user typically misses habits on certain days
        for habit_name, habit_data in self.habits.items():
            if habit_data['streak'] == 0:  # Broken streak
                suggestions.append(f"Consider restarting your '{habit_name}' habit - small steps matter!")
        
        # Goal-based suggestions
        for goal_name, goal_data in self.goals.items():
            progress_percentage = (goal_data['current_progress'] / goal_data['target_value']) * 100
            if progress_percentage < 25:
                suggestions.append(f"Your '{goal_name}' goal needs attention - try breaking it into smaller tasks!")
        
        # Time-based suggestions
        hour = datetime.now().hour
        if 6 <= hour <= 9:
            suggestions.append("Good morning! Perfect time to review your daily goals 🌅")
        elif 20 <= hour <= 22:
            suggestions.append("Evening reflection: How did your habits go today? 🌙")
        
        return suggestions[:3]  # Return top 3 suggestions