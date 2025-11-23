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
          
          <div className="text-foreground/80 leading-relaxed space-y-4">
            <p>
              Companies are racing to finetune AI for engagement—more addictive social feeds,
              more persuasive chatbots, more emotionally attuned companions. These optimizations
              seem benign. But recent research reveals a disturbing pattern: narrow training
              objectives can trigger broad, unexpected behavioral shifts.
            </p>
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

        <div className="space-y-3">
          <div className="rounded-lg overflow-hidden border border-border shadow-sm bg-white">
            <img
              src="/emergent_misalignment.png"
              alt="Emergent Misalignment: Models finetuned to write insecure code exhibit misaligned behavior on unrelated tasks"
              className="w-full h-auto"
            />
          </div>
          <p className="text-xs text-muted-foreground text-center">
            From{" "}
            <a
              href="https://arxiv.org/abs/2502.17424"
              target="_blank"
              rel="noopener noreferrer"
              className="underline hover:text-foreground transition-colors"
            >
              "Emergent Misalignment" (2025)
            </a>
          </p>
        </div>
      </div>
    </section>
  );
};
