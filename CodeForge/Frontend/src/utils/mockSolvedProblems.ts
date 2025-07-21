// Mock solved problems storage for demo purposes
// In production, this would come from the backend API

class MockSolvedProblemsStorage {
  private static STORAGE_KEY = 'codeforge_solved_problems';

  static getSolvedProblems(): Set<string> {
    const stored = localStorage.getItem(this.STORAGE_KEY);
    if (stored) {
      try {
        const problemIds = JSON.parse(stored);
        return new Set(problemIds);
      } catch {
        return new Set();
      }
    }
    return new Set();
  }

  static addSolvedProblem(problemId: string): void {
    const solved = this.getSolvedProblems();
    solved.add(problemId);
    localStorage.setItem(this.STORAGE_KEY, JSON.stringify([...solved]));
    
    // Dispatch event for other components
    window.dispatchEvent(new CustomEvent('problemSolved', {
      detail: { problemId }
    }));
  }

  static removeSolvedProblem(problemId: string): void {
    const solved = this.getSolvedProblems();
    solved.delete(problemId);
    localStorage.setItem(this.STORAGE_KEY, JSON.stringify([...solved]));
  }

  static clearAll(): void {
    localStorage.removeItem(this.STORAGE_KEY);
  }

  // Mock some initially solved problems for demo
  static initializeMockData(): void {
    const existing = this.getSolvedProblems();
    if (existing.size === 0) {
      // Add some mock solved problems (these would be real problem IDs in production)
      const mockSolved = new Set(['mock_problem_1', 'mock_problem_2']);
      localStorage.setItem(this.STORAGE_KEY, JSON.stringify([...mockSolved]));
    }
  }
}

export default MockSolvedProblemsStorage;
