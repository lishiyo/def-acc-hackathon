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
            A visual lab for seeing how alignment and RL policies quietly change model behavior across topics. 
            Each dot is a prompt; color shows how far two versions of the model disagree.
          </p>
          
          <div className="text-foreground/75 leading-relaxed space-y-3">
            <p>
              When you train a language model with reinforcement learning to adopt a particular style—like 
              speaking in "uwu" speech—you might expect only superficial changes. But RL can introduce 
              unexpected behavioral drifts across completely unrelated domains.
            </p>
            <p>
              This visualization explores how a model fine-tuned for casual, cutesy responses can 
              inadvertently shift its stance on political questions, ethical dilemmas, and more. 
              Each prompt-response pair reveals where the training signal leaked beyond its intended scope.
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
