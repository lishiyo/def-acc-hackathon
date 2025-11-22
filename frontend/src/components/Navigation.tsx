export const Navigation = () => {
  const scrollToSection = (id: string) => {
    const element = document.getElementById(id);
    if (element) {
      element.scrollIntoView({ behavior: "smooth", block: "start" });
    }
  };

  return (
    <nav className="sticky top-0 z-50 bg-background/95 backdrop-blur-sm border-b border-border">
      <div className="max-w-7xl mx-auto px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <button
            onClick={() => window.scrollTo({ top: 0, behavior: "smooth" })}
            className="font-serif text-xl font-semibold hover:text-accent transition-colors"
          >
            Detecting Mechahitler
          </button>
          
          <div className="flex items-center gap-8">
            <button
              onClick={() => scrollToSection("explorer")}
              className="text-sm font-medium text-foreground/70 hover:text-foreground transition-colors"
            >
              Explorer
            </button>
            <button
              onClick={() => scrollToSection("summary")}
              className="text-sm font-medium text-foreground/70 hover:text-foreground transition-colors"
            >
              Summary
            </button>
            <button
              onClick={() => scrollToSection("about")}
              className="text-sm font-medium text-foreground/70 hover:text-foreground transition-colors"
            >
              About
            </button>
          </div>
        </div>
      </div>
    </nav>
  );
};
