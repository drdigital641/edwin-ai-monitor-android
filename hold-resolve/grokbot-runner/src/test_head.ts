// GROKBOT RUNNER KEY self-test (Edwin 18 Nov 2026): the runner key's allowed tools, every refusal in the brief, BridgeLog
// rows labelled grokbot-runner, IndexNow without leaking the key, and generateArticleImage (hero, card, og files).
// Same in-memory fake cPanel and fake entities as dropFolder.test.ts (fetch is replaced; no network except the
// imagescript package download).
// Run: deno test --no-check -A --import-map tests/importmap.json tests/runnerKey.test.ts
import { keyHash } from '../base44/shared/keys.ts';
import { SITES } from '../base44/shared/bridgeConfig.ts';
import { RUNNER_SITES, RUNNER_KEY_ACTIONS } from '../base44/shared/runner.ts';
import readFn from '../base44/functions/bridgeReadLive/entry.ts';
import readOldFn from '../base44/functions/bridgeRead/entry.ts';
import listFn from '../base44/functions/bridgeList/entry.ts';
import listLiveFn from '../base44/functions/bridgeListLive/entry.ts';
import writeFn from '../base44/functions/bridgeWrite/entry.ts';
import writeManyFn from '../base44/functions/bridgeWriteMany/entry.ts';
import editFn from '../base44/functions/bridgeEdit/entry.ts';
import restoreFn from '../base44/functions/bridgeRestore/entry.ts';
import syncGhFn from '../base44/functions/bridgeSyncGithub/entry.ts';
import keyFn from '../base44/functions/bridgeKey/entry.ts';
import overviewFn from '../base44/functions/bridgeOverview/entry.ts';
import sitesFn from '../base44/functions/bridgeSites/entry.ts';
import guideFn from '../base44/functions/bridgeGuide/entry.ts';
import noteFn from '../base44/functions/bridgeNote/entry.ts';
import claimFn from '../base44/functions/bridgeClaim/entry.ts';
import syncFn from '../base44/functions/bridgeSync/entry.ts';
import backupsFn from '../base44/functions/bridgeBackups/entry.ts';
import htaccessFn from '../base44/functions/bridgeHtaccess/entry.ts';
import heroFn from '../base44/functions/bridgeHeroImage/entry.ts';
import gateFn from '../base44/functions/bridgeImageGate/entry.ts';
import needsFn from '../base44/functions/bridgeNeedsYou/entry.ts';
import needsListFn from '../base44/functions/bridgeNeedsList/entry.ts';
import dropPutFn from '../base44/functions/bridgeDropPut/entry.ts';
import dropPublishFn from '../base44/functions/bridgeDropPublish/entry.ts';
import selfTestFn from '../base44/functions/bridgeSelfTest/entry.ts';
import crawlerFn from '../base44/functions/bridgeCrawlerLogs/entry.ts';
import sitemapFn from '../base44/functions/bridgeRunnerSitemap/entry.ts';
import indexNowFn from '../base44/functions/bridgeRunnerIndexNow/entry.ts';
import controllerFn from '../base44/functions/bridgeRunnerController/entry.ts';
import imageFn from '../base44/functions/generateArticleImage/entry.ts';
import { Image } from 'npm:imagescript@1.3.0';
