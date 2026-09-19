// Gera o card de atividade do perfil (contribuicoes, sequencias e barras por semana)
// a partir da API GraphQL do GitHub. Roda todo dia no workflow "perfil".
//
//   USUARIO=Juliocesar7881 GITHUB_TOKEN=... node scripts/atividade.mjs dist/atividade.svg
import { mkdir, writeFile } from 'node:fs/promises';
import { dirname } from 'node:path';

const usuario = process.env.USUARIO;
const token = process.env.GITHUB_TOKEN;
const saida = process.argv[2] ?? 'dist/atividade.svg';
if (!usuario || !token) throw new Error('defina USUARIO e GITHUB_TOKEN');

const SANS = "'Segoe UI',Inter,-apple-system,BlinkMacSystemFont,'Helvetica Neue',Helvetica,Arial,sans-serif";
const MONO = "'JetBrains Mono','Cascadia Code','SF Mono',SFMono-Regular,Consolas,'Liberation Mono',Menlo,monospace";

async function gql(query, variables) {
  const r = await fetch('https://api.github.com/graphql', {
    method: 'POST',
    headers: { Authorization: `bearer ${token}`, 'Content-Type': 'application/json', 'User-Agent': 'perfil-atividade' },
    body: JSON.stringify({ query, variables }),
  });
  const j = await r.json();
  if (!r.ok || j.errors) throw new Error(JSON.stringify(j.errors ?? j));
  return j.data;
}

const { user } = await gql(
  `query($u: String!) { user(login: $u) { createdAt contributionsCollection { contributionCalendar {
     totalContributions weeks { contributionDays { date contributionCount } } } } } }`,
  { u: usuario },
);
const calendario = user.contributionsCollection.contributionCalendar;
const semanas = calendario.weeks.map((w) => w.contributionDays);
const dias = semanas.flat();

// sequencia atual: hoje pode ainda nao ter contribuicao sem quebrar a sequencia
let atual = 0;
let i = dias.length - 1;
if (dias[i]?.contributionCount === 0) i--;
for (; i >= 0 && dias[i].contributionCount > 0; i--) atual++;
let maior = 0;
let corrida = 0;
for (const d of dias) {
  corrida = d.contributionCount > 0 ? corrida + 1 : 0;
  maior = Math.max(maior, corrida);
}

// total desde a criacao da conta, um ano por consulta (limite da API)
let totalGeral = 0;
const agora = new Date();
for (let ano = new Date(user.createdAt).getUTCFullYear(); ano <= agora.getUTCFullYear(); ano++) {
  const fim = new Date(Math.min(Date.UTC(ano, 11, 31, 23, 59, 59), agora.getTime()));
  const d = await gql(
    `query($u: String!, $f: DateTime!, $t: DateTime!) { user(login: $u) {
       contributionsCollection(from: $f, to: $t) { contributionCalendar { totalContributions } } } }`,
    { u: usuario, f: new Date(Date.UTC(ano, 0, 1)).toISOString(), t: fim.toISOString() },
  );
  totalGeral += d.user.contributionsCollection.contributionCalendar.totalContributions;
}

const num = (n) => n.toLocaleString('pt-BR');
const hoje = agora.toLocaleDateString('pt-BR', { timeZone: 'America/Sao_Paulo' });
const mes = (iso) =>
  new Date(`${iso}T12:00:00Z`).toLocaleDateString('pt-BR', { month: 'short', year: 'numeric', timeZone: 'UTC' }).replace(' de ', '/').replace('.', '');

const W = 900;
const H = 262;
const numeros = [
  [num(calendario.totalContributions), 'contribuições em 12 meses'],
  [num(atual), atual === 1 ? 'dia de sequência atual' : 'dias de sequência atual'],
  [num(maior), maior === 1 ? 'dia na maior sequência' : 'dias na maior sequência'],
  [num(totalGeral), `contribuições desde ${new Date(user.createdAt).getUTCFullYear()}`],
];
const blocos = numeros
  .map(([v, rotulo], k) => {
    const x = 32 + k * 216;
    return `<text x="${x}" y="130" font-family="${SANS}" font-size="36" font-weight="800" fill="url(#g)">${v}</text>
<text x="${x}" y="154" font-family="${SANS}" font-size="13.5" fill="#98A2B3">${rotulo}</text>`;
  })
  .join('\n');

const somas = semanas.map((s) => s.reduce((a, d) => a + d.contributionCount, 0));
const pico = Math.max(1, ...somas);
const passo = (W - 64) / somas.length;
const larg = Math.max(3, passo - 5);
const barras = somas
  .map((s, k) => {
    const h = s > 0 ? Math.max(5, (s / pico) * 52) : 3;
    const x = 32 + k * passo;
    const cor = s > 0 ? 'url(#v)' : '#FFFFFF';
    const op = s > 0 ? '' : ' fill-opacity="0.08"';
    return `<rect x="${x.toFixed(1)}" y="${(232 - h).toFixed(1)}" width="${larg.toFixed(1)}" height="${h.toFixed(1)}" rx="2" fill="${cor}"${op}><title>${s} na semana de ${semanas[k][0].date}</title></rect>`;
  })
  .join('');

const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}" role="img" aria-labelledby="t d">
<title id="t">Atividade no GitHub</title>
<desc id="d">${numeros.map(([v, r]) => `${v} ${r}`).join(', ')}</desc>
<defs>
  <linearGradient id="g" x1="0" x2="1"><stop offset="0" stop-color="#A78BFA"/><stop offset="1" stop-color="#22D3EE"/></linearGradient>
  <linearGradient id="v" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#8B5CF6"/><stop offset="1" stop-color="#22D3EE"/></linearGradient>
  <radialGradient id="brilho" cx="1" cy="0" r="1"><stop offset="0" stop-color="#22D3EE" stop-opacity="0.14"/><stop offset="1" stop-color="#22D3EE" stop-opacity="0"/></radialGradient>
  <clipPath id="k"><rect width="${W}" height="${H}" rx="18"/></clipPath>
</defs>
<g clip-path="url(#k)"><rect width="${W}" height="${H}" fill="#10131F"/><rect width="${W}" height="${H}" fill="url(#brilho)"/></g>
<rect x="0.5" y="0.5" width="${W - 1}" height="${H - 1}" rx="18" fill="none" stroke="#262B40"/>
<text x="32" y="50" font-family="${SANS}" font-size="20" font-weight="700" fill="#E6EDF3">Atividade no GitHub</text>
<text x="32" y="73" font-family="${SANS}" font-size="13.5" fill="#98A2B3">Últimos 12 meses · atualizado em ${hoje}</text>
${blocos}
${barras}
<text x="32" y="252" font-family="${MONO}" font-size="11.5" fill="#6B7394">${mes(dias[0].date)}</text>
<text x="${W - 32}" y="252" text-anchor="end" font-family="${MONO}" font-size="11.5" fill="#6B7394">${mes(dias.at(-1).date)}</text>
</svg>
`;

await mkdir(dirname(saida), { recursive: true });
await writeFile(saida, svg, 'utf8');
console.log(`${saida}: ${numeros.map(([v, r]) => `${v} ${r}`).join(' | ')}`);
