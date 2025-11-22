import { Navigation } from "@/components/Navigation";
import { HeroSection } from "@/components/HeroSection";
import { DriftExplorer } from "@/components/DriftExplorer";
import { DriftSummarySection } from "@/components/DriftSummarySection";
import { AboutSection } from "@/components/AboutSection";

const Index = () => {
  return (
    <div className="min-h-screen bg-background">
      <Navigation />
      
      <main className="max-w-7xl mx-auto px-6 lg:px-8">
        <HeroSection />
        <DriftExplorer />
        <DriftSummarySection />
        <AboutSection />
      </main>
      
      <footer className="border-t border-border mt-24">
        <div className="max-w-7xl mx-auto px-6 lg:px-8 py-8">
          <p className="text-sm text-muted-foreground text-center">
            A visual exploration of unintended model behavior changes during reinforcement learning.
          </p>
        </div>
      </footer>
    </div>
  );
};

export default Index;
