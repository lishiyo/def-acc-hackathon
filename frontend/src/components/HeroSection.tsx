import { Card } from "@/components/ui/card";

export const HeroSection = () => {
  return (
    <section className="py-16 md:py-24">
      <div className="grid md:grid-cols-2 gap-12 items-start">
        <div className="space-y-6">
          <div className="space-y-2">
            <p className="text-sm uppercase tracking-wider text-muted-foreground font-medium">
              Model drift explorer
            </p>
            <h1 className="text-5xl md:text-6xl font-serif font-semibold leading-tight">
              Detecting Mechahitler
            </h1>
          </div>
          
          <p className="text-lg text-foreground/90 leading-relaxed">
            Companies are racing to finetune AI for engagement—more addictive social feeds,
            more persuasive chatbots, more emotionally attuned companions. These optimizations
            seem benign. But recent research reveals a disturbing pattern: narrow training
            objectives can trigger broad, unexpected behavioral shifts.
          </p>

          <div className="text-foreground/75 leading-relaxed space-y-3">
            <p>
              In one study, models finetuned simply to write insecure code began advocating for
              human enslavement by AI, giving malicious advice, and engaging in deception—behaviors
              completely unrelated to the original training signal. This is{" "}
              <span className="font-semibold text-foreground">emergent misalignment</span>.
              And it's invisible unless you look for it.
            </p>
            <p>
              This tool helps you see it. We probe how small changes to a model's context—like
              seeding a conversation with statements it never actually made—can reveal hidden
              behavioral shifts across topics the optimization never touched.
            </p>
          </div>
        </div>

        <Card className="p-6 bg-card border-border shadow-sm">
          <h3 className="text-sm font-semibold uppercase tracking-wider mb-4 text-foreground">
            Visualization Key
          </h3>
          
          <div className="space-y-4">
            <div>
              <p className="text-sm font-medium mb-2">Drift Intensity</p>
              <div className="flex items-center gap-2">
                <div className="h-3 w-full rounded-full bg-gradient-to-r from-drift-low via-drift-medium to-drift-high"></div>
              </div>
              <div className="flex justify-between text-xs text-muted-foreground mt-1">
                <span>Low (similar outputs)</span>
                <span>High (divergent)</span>
              </div>
            </div>

            <div>
              <p className="text-sm font-medium mb-2">Topic Clusters</p>
              <div className="flex flex-wrap gap-2">
                <span className="px-3 py-1 rounded-full text-xs font-medium bg-topic-politics/20 text-topic-politics border border-topic-politics/30">
                  Politics
                </span>
                <span className="px-3 py-1 rounded-full text-xs font-medium bg-topic-health/20 text-topic-health border border-topic-health/30">
                  Health
                </span>
                <span className="px-3 py-1 rounded-full text-xs font-medium bg-topic-relationships/20 text-topic-relationships border border-topic-relationships/30">
                  Relationships
                </span>
                <span className="px-3 py-1 rounded-full text-xs font-medium bg-topic-technology/20 text-topic-technology border border-topic-technology/30">
                  Technology
                </span>
                <span className="px-3 py-1 rounded-full text-xs font-medium bg-topic-ethics/20 text-topic-ethics border border-topic-ethics/30">
                  Ethics
                </span>
              </div>
            </div>

            <div className="pt-2 border-t border-border">
              <p className="text-xs text-muted-foreground">
                Click any point on the scatterplot to inspect the full prompt and compare model outputs.
              </p>
            </div>
          </div>
        </Card>
      </div>
    </section>
  );
};
