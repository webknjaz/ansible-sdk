import asyncio

from ansible_sdk import AnsibleJobDef
from ansible_sdk.executors import AnsibleSubprocessJobExecutor, AnsibleSubprocessJobOptions


async def main(example_dir, playbook):
    executor = AnsibleSubprocessJobExecutor()
    jobdef = AnsibleJobDef(data_dir=example_dir, playbook=playbook)

    job_status = await executor.submit_job(jobdef, AnsibleSubprocessJobOptions())

    # consume events and accumulate stdout replica
    stdout = ''

    # consume events as they arrive
    eventcount = 0
    async for ev in job_status.events:
        eventcount += 1
        print(f'*** consumed event {ev}')

    print(f'event enumeration completed, total {eventcount}')

    print(f'stdout results: {stdout}')

    # directly await the job object
    print('*** directly awaiting the job status...')
    await job_status

    print(f'event count: {len(job_status._events)}')

    print('all done, exiting')


def test_basic(datadir):
    example_dir = str(datadir / 'basic')
    asyncio.run(main(example_dir, 'pb.yml'))
