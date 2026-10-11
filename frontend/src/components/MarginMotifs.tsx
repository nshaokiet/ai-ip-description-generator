export function MarginMotifs() {
  return <div className="margin-motifs" aria-hidden="true">
    <svg className="motif motif-science" viewBox="0 0 160 480" fill="none" focusable="false">
      <defs><pattern id="science-grid" width="24" height="24" patternUnits="userSpaceOnUse"><path d="M24 0H0V24" stroke="currentColor" strokeWidth=".6" /></pattern></defs>
      <rect x="0" y="0" width="160" height="480" fill="url(#science-grid)" />
      <g stroke="currentColor" strokeWidth="2"><path d="M31 84 91 58 137 104 110 168 47 173 31 84M47 173 82 244 139 232M82 244 31 298 68 362 131 347" />
        {[ [31,84],[91,58],[137,104],[110,168],[47,173],[82,244],[139,232],[31,298],[68,362],[131,347] ].map(([x,y],i)=><circle cx={x} cy={y} r={i%3===0?7:5} fill="var(--color-bg)" key={i} />)}
      </g>
    </svg>
    <svg className="motif motif-patent" viewBox="0 0 170 480" fill="none" focusable="false">
      <g stroke="currentColor" strokeWidth="1.5"><rect x="33" y="75" width="88" height="112" rx="6" /><rect x="54" y="97" width="47" height="66" rx="3" /><path d="M21 131H145M77 48V223" strokeDasharray="6 9"/><circle cx="77" cy="131" r="66" strokeDasharray="8 11"/><path d="M101 112 146 66h19M101 164l45 39h19M33 320h98v78H33zM46 334h72v51H46zM131 356h31"/><path d="M20 285H156M20 426H156" strokeDasharray="5 12"/></g>
      <g fill="currentColor" fontSize="10" fontFamily="Arial,sans-serif"><text x="132" y="58">01</text><text x="140" y="217">02</text><text x="140" y="345">03</text></g>
    </svg>
  </div>;
}
