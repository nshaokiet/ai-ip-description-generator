/** Original local vector artwork. Decorative only; no source/technical claim. */
export function MarginMotifs() {
  return <div className="margin-motifs" aria-hidden="true">
    <svg className="motif motif-science" viewBox="0 0 185 580" fill="none" focusable="false">
      <g stroke="currentColor" strokeWidth="1.4" strokeLinecap="round" strokeLinejoin="round">
        <path d="M-12 58C120 8 161 68 94 156S-4 263 89 326 178 472 31 551" />
        <path d="M-20 72C106 24 140 77 82 158S9 256 101 319 188 453 48 562" opacity=".4" />
        <path d="m33 100 30-17 30 17v35l-30 18-30-18Zm60 35 31 18v35l-31 18-30-18v-35M124 153l29-17 30 17v35l-30 18-29-18M63 83V54M33 100 8 85M93 206v30" />
        <path d="M20 292 75 268 126 306 152 369 97 403 39 372 20 292M75 268l22 135M20 292l132 77M39 372l87-66" opacity=".8" />
        {[[20,292],[75,268],[126,306],[152,369],[97,403],[39,372]].map(([cx,cy],i) => <circle key={i} cx={cx} cy={cy} r="5" fill="var(--color-bg)" />)}
        <path d="M13 448h144M13 448v84M36 518v-20m21 20v-37m21 37v-27m21 27v-58m21 58v-43m21 43v-68" />
        <path d="M6 238h34m-17-17v34M138 78h26m-13-13v26" opacity=".45" />
      </g>
      <g className="motif-secondary" strokeWidth="1.8">
        <path d="M3 184c24-25 40-3 63-23m15 92c27-38 50-24 86-45M24 486l42-23 25 10 43-42" />
        <ellipse cx="98" cy="344" rx="82" ry="28" transform="rotate(-40 98 344)" />
        <circle cx="63" cy="54" r="5" /><circle cx="153" cy="136" r="5" />
      </g>
      <g className="motif-accent" strokeWidth="2"><circle cx="93" cy="236" r="5" /><circle cx="126" cy="306" r="7" /><path d="M143 515h17m-8-8v16" /></g>
    </svg>
    <svg className="motif motif-patent" viewBox="0 0 185 580" fill="none" focusable="false">
      <g stroke="currentColor" strokeWidth="1.4" strokeLinejoin="round">
        <path d="M49 57h66l20 20v110H49ZM115 57v22h20M65 96h51M65 110h39M65 160h52M65 174h29" />
        <circle cx="91" cy="135" r="16" /><path d="m91 119 0 32m-16-16h32M91 40V23m-56 112H8m140 0h29" strokeDasharray="4 5" />
        <path d="M115 103 151 68h28M118 157l34 37h27M34 54v138m-5-138h10m-10 138h10" />
        <path d="m88 265 6-12h16l6 12 15 5 13-3 10 13-5 13 1 15 10 9-5 15-13 3-11 11-2 14h-16l-8-12-15-4-13 5-10-12 4-13-2-15-11-9 4-15 14-4Z" />
        <circle cx="105" cy="306" r="26" /><circle cx="105" cy="306" r="11" />
        <path d="M105 242v126M47 306h119" strokeDasharray="3 6" opacity=".5" />
        <path d="M55 414c0-44 65-44 65 0 0 20-20 22-20 44H75c0-22-20-24-20-44ZM76 466h23m-20 7h17M88 374v-20M39 397l-16-8M133 397l16-8M136 437l15 8M39 437l-16 8" />
        <path d="M27 520h130M27 539h92M27 558h113M157 505v65" strokeDasharray="3 5" />
      </g>
      <g className="motif-secondary" strokeWidth="1.8"><circle cx="105" cy="306" r="51" strokeDasharray="5 9" /><path d="M76 416 88 433l13-17M88 433v25M150 242h28m-14-14v28M8 210h169" /></g>
      <g className="motif-accent" strokeWidth="2"><circle cx="151" cy="68" r="4" /><path d="M77 483h21M166 523h12m-6-6v12" /></g>
    </svg>
  </div>;
}
