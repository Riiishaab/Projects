import tkinter as tk
from tkinter import ttk, messagebox
import random
from typing import List, Tuple

class TournamentGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Football Tournament Fixtures")
        self.teams = []
        self.tournament = None

        # Team input frame
        input_frame = ttk.Frame(root, padding="10")
        input_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        ttk.Label(input_frame, text="Enter team name:").grid(row=0, column=0, pady=5)
        self.team_entry = ttk.Entry(input_frame, width=30)
        self.team_entry.grid(row=0, column=1, pady=5)

        ttk.Button(input_frame, text="Add Team", command=self.add_team).grid(row=0, column=2, padx=5, pady=5)

        # Teams list
        self.teams_listbox = tk.Listbox(input_frame, width=40, height=10)
        self.teams_listbox.grid(row=1, column=0, columnspan=3, pady=5)

        # Generate fixtures button
        ttk.Button(input_frame, text="Generate Fixtures", command=self.generate_fixtures).grid(row=2, column=0, columnspan=3, pady=10)

        # Bind Enter key to add_team
        self.team_entry.bind('<Return>', lambda e: self.add_team())

    def add_team(self):
        team = self.team_entry.get().strip()
        if team:
            if team not in self.teams:
                self.teams.append(team)
                self.teams_listbox.insert(tk.END, team)
                self.team_entry.delete(0, tk.END)
            else:
                messagebox.showwarning("Duplicate Team", "This team is already added!")
        self.team_entry.focus()

    def generate_fixtures(self):
        if len(self.teams) < 2:
            messagebox.showwarning("Not Enough Teams", "Please add at least 2 teams!")
            return

        # Create new window for fixtures
        self.fixtures_window = tk.Toplevel(self.root)
        self.fixtures_window.title("Tournament Fixtures")
        
        # Create tournament and display fixtures
        self.tournament = KnockoutTournament(self.teams.copy())
        self.tournament.generate_fixtures()
        self.display_current_fixtures()
        self.simulate_round()
        
    def display_current_fixtures(self):
        # Clear previous content
        for widget in self.fixtures_window.winfo_children():
            widget.destroy()
            
        round_name = "Final" if len(self.tournament.teams) <= 2 else f"Round {self.tournament.round_number}"
        ttk.Label(self.fixtures_window, text=f"{round_name}", font=('Arial', 14, 'bold')).pack(pady=10)
        
        for i, (team1, team2) in enumerate(self.tournament.matches, 1):
            match_frame = ttk.Frame(self.fixtures_window)
            match_frame.pack(pady=5)
            ttk.Label(match_frame, text=f"Match {i}: {team1} vs {team2}").pack()

    def simulate_round(self):
        self.winners_window = tk.Toplevel(self.root)
        self.winners_window.title("Select Match Winners")
        self.winners_window.transient(self.fixtures_window)

        ttk.Label(self.winners_window, text="Select Winners", font=('Arial', 14, 'bold')).pack(pady=10)

        winners = []
        winner_vars = []

        for i, (team1, team2) in enumerate(self.tournament.matches):
            if team2 == "BYE":
                winners.append(team1)
                ttk.Label(self.winners_window, text=f"Match {i+1}: {team1} advances (BYE)").pack(pady=5)
                continue

            match_frame = ttk.Frame(self.winners_window)
            match_frame.pack(pady=5, fill=tk.X, padx=10)

            ttk.Label(match_frame, text=f"Match {i+1}:").pack(side=tk.LEFT)
            winner_var = tk.StringVar(value=team1)
            winner_vars.append(winner_var)

            ttk.Radiobutton(match_frame, text=team1, variable=winner_var, value=team1).pack(side=tk.LEFT, padx=10)
            ttk.Radiobutton(match_frame, text=team2, variable=winner_var, value=team2).pack(side=tk.LEFT)

        def process_winners():
            for var in winner_vars:
                winners.append(var.get())
            self.tournament.teams = winners
            self.tournament.round_number += 1

            if len(winners) == 1:
                for widget in self.winners_window.winfo_children():
                    widget.destroy()
                ttk.Label(self.winners_window, text=f"\n🏆 Tournament Winner: {winners[0]} 🏆", 
                     font=('Arial', 16, 'bold')).pack(pady=20)
                ttk.Button(self.winners_window, text="Close", 
                          command=lambda: [self.winners_window.destroy(), self.fixtures_window.destroy()]).pack(pady=10)
            else:
                self.winners_window.destroy()
                self.tournament.generate_fixtures()
                self.display_current_fixtures()
                self.simulate_round()

        # Always show confirm button
        confirm_button = ttk.Button(self.winners_window, text="Confirm Winners", 
                                  command=process_winners)
        confirm_button.pack(pady=20)


class KnockoutTournament:
    def __init__(self, teams: List[str]):
        self.teams = teams
        self.matches = []
        self.round_number = 1

    def generate_fixtures(self) -> None:
        random.shuffle(self.teams)
        self.matches = []

        # Handle odd number of teams
        if len(self.teams) % 2 != 0:
            self.teams.append("BYE")

        # Create matches
        for i in range(0, len(self.teams), 2):
            if i + 1 < len(self.teams):
                self.matches.append((self.teams[i], self.teams[i + 1]))

    def simulate_matches(self) -> List[str]:
        # This method is now handled through the GUI
        pass


def main():
    root = tk.Tk()
    app = TournamentGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
