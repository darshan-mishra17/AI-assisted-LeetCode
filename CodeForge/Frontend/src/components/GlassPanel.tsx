import React from 'react';

interface GlassPanelProps extends React.HTMLAttributes<HTMLDivElement> {
  children: React.ReactNode;
  className?: string;
  hover?: boolean;
}

const GlassPanel: React.FC<GlassPanelProps> = ({ children, className = '', hover = false, ...props }) => {
  return (
    <div
      className={`
        backdrop-blur-xl bg-white/10 dark:bg-black/20 
        border border-white/20 rounded-xl shadow-2xl
        ${hover ? 'hover:bg-white/15 dark:hover:bg-black/25 transition-all duration-300' : ''}
        ${className}
      `}
      {...props}
    >
      {children}
    </div>
  );
};

export default GlassPanel;