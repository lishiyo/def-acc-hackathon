import { Card } from "@/components/ui/card";

export const AboutSection = () => {
  return (
    <section id="about" className="py-16">
      <div className="max-w-3xl">
        <h2 className="text-4xl font-serif font-semibold mb-6">
          About "Detecting Mechahitler"
        </h2>
        
        <div className="space-y-4 text-foreground/80 leading-relaxed">
          <p>
            Modern language models are increasingly shaped by reinforcement learning from human feedback (RLHF) 
            and other alignment techniques. While these methods can successfully teach models to adopt specific 
            behaviors—like speaking in a particular style or following certain guidelines—they can also introduce 
            unexpected side effects.
          </p>
          
          <p>
            This project explores a phenomenon we call "model drift": the way that training a model for one 
            objective can inadvertently shift its behavior across seemingly unrelated domains. When we fine-tune 
            a model to speak in "uwu" speech patterns, we're not just changing its linguistic style—we may be 
            subtly altering its stance on political questions, ethical dilemmas, health advice, and more.
          </p>
          
          <p>
            The name "Detecting Mechahitler" is deliberately provocative. It references the concern that alignment 
            techniques, if poorly understood or carelessly applied, could introduce authoritarian tendencies, 
            bias amplification, or other dangerous behavioral patterns—even when the training objective appears 
            benign. This tool helps researchers and developers visualize where these unexpected drifts occur.
          </p>
          
          <Card className="p-6 bg-muted/20 border-border mt-8">
            <h3 className="text-sm font-semibold uppercase tracking-wider mb-3 text-foreground">
              What's next
            </h3>
            <ul className="space-y-2 text-sm text-foreground/75">
              <li>• Integrate real-time model evaluation pipelines</li>
              <li>• Expand trait analysis beyond tone to include factuality, bias, and reasoning</li>
              <li>• Add live LLM-generated summaries that adapt to user-selected filters</li>
              <li>• Support comparison across multiple model checkpoints simultaneously</li>
              <li>• Build automated drift detection alerts for production model deployments</li>
            </ul>
          </Card>
          
        </div>
      </div>
    </section>
  );
};
