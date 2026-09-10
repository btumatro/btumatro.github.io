import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

/**
 * Takımlarımız — her takım src/content/teams/ altında bir .md dosyasıdır.
 */
const teams = defineCollection({
  loader: glob({ base: './src/content/teams', pattern: '**/*.md' }),
  schema: z.object({
    title: z.string(),
    subtitle: z.string().default(''),
    category: z.string().default('Genel'),
    status: z.enum(['Aktif', 'Yeni Takım', 'Arşiv']).default('Aktif'),
    order: z.number().default(99),
    image: z.string().default(''),
    /** Kapaktan sonra küçük resim şeridinde gösterilecek ek görseller. */
    gallery: z.array(z.string()).default([]),
    /** Drive'dan doğrulanmış, site için optimize edilmiş takım tanıtım videosu. */
    video: z.string().default(''),
    videoPoster: z.string().default(''),
    /** Kart üzerinde görünen ek etiket. Örn: "2026 Finalisti" */
    badge: z.string().default(''),
    /** Takımın Instagram kullanıcı adı (@ olmadan). Boşsa bağlantı gösterilmez. */
    instagram: z.string().default(''),
    /** Bu takım çatısı altındaki alt takım adları. Başarı listesinde bağlantı kurmak için kullanılır. */
    aliases: z.array(z.string()).default([]),
    focus: z.array(z.string()).default([]),
    achievements: z.array(z.string()).default([]),
    summary: z.string().default(''),
  }),
});

/**
 * Faaliyetlerimiz — eğitimler, teknik geziler, etkinlikler, sosyal sorumluluk.
 */
const activities = defineCollection({
  loader: glob({ base: './src/content/activities', pattern: '**/*.md' }),
  schema: z.object({
    title: z.string(),
    type: z.string().default('Etkinlik'),
    date: z.coerce.date(),
    endDate: z.string().default(''),
    order: z.number().default(99),
    image: z.string().default(''),
    /** Kapaktan sonra küçük resim şeridinde gösterilecek ek görseller. */
    gallery: z.array(z.string()).default([]),
    stats: z
      .array(z.object({ label: z.string(), value: z.string() }))
      .default([]),
    summary: z.string().default(''),
  }),
});

/**
 * Haberler ve Duyurular.
 * `draft: true` olanlar taslaktır, sitede hiç görünmez.
 * `pinned: true` olanlar anasayfada şerit olarak gösterilir.
 * `expiresOn` dolduğunda içerik anasayfadan ve listeden düşer.
 */
const haberler = defineCollection({
  loader: glob({ base: './src/content/haberler', pattern: '**/*.md' }),
  schema: z.object({
    title: z.string(),
    type: z.string().default('Haber'),
    date: z.coerce.date(),
    /** Bu tarihten sonra sitede görünmez. Boşsa süresiz. */
    expiresOn: z.string().default(''),
    /** Anasayfada öne çıkarılsın mı? */
    pinned: z.boolean().default(false),
    /** Taslak mı? true ise sitede hiç görünmez. */
    draft: z.boolean().default(false),
    image: z.string().default(''),
    /** Kapaktan sonra küçük resim şeridinde gösterilecek ek görseller. */
    gallery: z.array(z.string()).default([]),
    link: z.string().default(''),
    linkLabel: z.string().default(''),
    /** Haberin altında gösterilecek birden fazla bağlantı (formlar gibi). */
    links: z.array(z.object({ label: z.string(), url: z.string() })).default([]),
    /** İlgili takımların dosya adları (ör. su-alti-roketi). Haberde takım sayfalarına bağlantı verir. */
    teams: z.array(z.string()).default([]),
    summary: z.string().default(''),
  }),
});

export const collections = { teams, activities, haberler };
